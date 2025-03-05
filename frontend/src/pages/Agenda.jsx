import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { FaTrash } from "react-icons/fa";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Agenda = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [servicos, setServicos] = useState([]);
  const [disponibilidades, setDisponibilidades] = useState([]);
  const [form, setForm] = useState({
    servicoId: "",
    inicio: new Date(),
    final: new Date(),
    duracao: 30,
    repetir: false,
    semanas: 1,
  });

  useEffect(() => {
    if (user?.role !== "prestador") {
      navigate("/dashboard");
    } else {
      carregarServicos();
      carregarDisponibilidades();
    }
  }, [user, navigate]);

  const carregarServicos = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://localhost:8000/servicos", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setServicos(response.data);
    } catch (error) {
      console.error("Erro ao carregar serviços", error);
    }
  };

  const handleRedirectToCalendar = () => {
    if (user?.email) {
      navigate(`/calendario/${user.email}`);
    }
  };

  const calcularHorarioFinal = () => {
    const dataFim = new Date(form.inicio);
    dataFim.setMinutes(dataFim.getMinutes() + form.duracao);
    return dataFim;
  };

  const carregarDisponibilidades = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(`http://localhost:8000/disponibilidade/prestador/${user.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setDisponibilidades(response.data);
    } catch (error) {
      console.error("Erro ao carregar disponibilidades", error);
    }
  };

  const agruparDisponibilidades = () => {
    const grupos = {};

    disponibilidades.forEach((disp) => {
      const dataInicio = new Date(disp.inicio);
      const mesAno = `${dataInicio.toLocaleString("pt-BR", { month: "long", year: "numeric" })}`;
      const servicoNome = disp.servico_nome;

      if (!grupos[mesAno]) {
        grupos[mesAno] = {};
      }
      if (!grupos[mesAno][servicoNome]) {
        grupos[mesAno][servicoNome] = [];
      }
      grupos[mesAno][servicoNome].push(disp);
    });

    return grupos;
  };

  const grupos = agruparDisponibilidades();
  const [mesAberto, setMesAberto] = useState(null);
  const [servicoAberto, setServicoAberto] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      let disponibilidades = [
        {
          servico_id: form.servicoId,
          inicio: form.inicio.toISOString(),
          final: calcularHorarioFinal().toISOString(),
        }
      ];
  
      if (form.repetir && form.semanas > 0) {
        for (let i = 1; i <= form.semanas; i++) {
          const novaDataInicio = new Date(form.inicio);
          novaDataInicio.setDate(novaDataInicio.getDate() + i * 7);
  
          // 🔹 Agora a data final é calculada corretamente com base na duração
          const novaDataFinal = new Date(novaDataInicio);
          novaDataFinal.setMinutes(novaDataFinal.getMinutes() + form.duracao);
  
          disponibilidades.push({
            servico_id: form.servicoId,
            inicio: novaDataInicio.toISOString(),
            final: novaDataFinal.toISOString(),
          });
        }
      }
  
      await axios.post("http://localhost:8000/disponibilidade/lote", disponibilidades, {
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      });
  
      carregarDisponibilidades();
    } catch (error) {
      console.error("Erro ao cadastrar disponibilidade", error);
    }
  };

  const handleDelete = async (id) => {
    try {
      const token = localStorage.getItem("token");

      await axios.delete(`http://localhost:8000/disponibilidade/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setDisponibilidades(disponibilidades.filter((disp) => disp.id !== id));
    } catch (error) {
      console.error("Erro ao excluir disponibilidade", error);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto bg-white shadow-md rounded-md">
      <h1 className="text-2xl font-bold mb-4">Gerenciar Disponibilidades</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <select
          name="servicoId"
          value={form.servicoId}
          onChange={(e) => setForm({ ...form, servicoId: e.target.value })}
          className="w-full p-2 border border-gray-300 rounded"
          required>
          <option value="">Selecione um serviço</option>
          {servicos.map((servico) => (
            <option key={servico.id} value={servico.id}>
              {servico.nome}
            </option>
          ))}
        </select>

        <div className="flex gap-4">
          <div>
            <label className="block font-medium">Início</label>
            <DatePicker
              selected={form.inicio}
              onChange={(date) => setForm({ ...form, inicio: date })}
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={30}
              dateFormat="Pp"
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div>
            <label className="block font-medium">Duração (minutos)</label>
            <input
              type="range"
              min="15"
              max="240"
              step="15"
              value={form.duracao}
              onChange={(e) => setForm({ ...form, duracao: parseInt(e.target.value) })}
              className="w-full cursor-pointer"
            />
            <p className="text-center">{form.duracao} minutos</p>
          </div>
        </div>

        <div className="flex items-center">
          <input
            type="checkbox"
            id="repetir"
            checked={form.repetir}
            onChange={(e) => setForm({ ...form, repetir: e.target.checked })}
            className="mr-2"
          />
          <label htmlFor="repetir" className="font-medium">Repetir semanalmente</label>
        </div>

        {form.repetir && (
          <div>
            <label className="block font-medium">Quantas semanas deseja repetir?</label>
            <input
              type="number"
              min="1"
              value={form.semanas}
              onChange={(e) => setForm({ ...form, semanas: parseInt(e.target.value) })}
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
        )}

        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Cadastrar Disponibilidade
        </button>
      </form>

      <button
        onClick={handleRedirectToCalendar}
        className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition mb-4">
        Ver meu calendário
      </button>

      <h2 className="text-xl font-semibold mt-6">Suas Disponibilidades</h2>
      <div className="mt-4">
        {Object.keys(grupos).map((mes) => (
          <div key={mes} className="mb-4">
            <button
              onClick={() => setMesAberto(mesAberto === mes ? null : mes)}
              className="w-full text-left font-bold text-lg bg-gray-200 p-2 rounded"
            >
              {mes} {mesAberto === mes ? "▲" : "▼"}
            </button>

            {mesAberto === mes && (
              <div className="ml-4 mt-2">
                {Object.keys(grupos[mes]).map((servico) => (
                  <div key={servico} className="mb-2">
                    <button
                      onClick={() => setServicoAberto(servicoAberto === servico ? null : servico)}
                      className="w-full text-left font-medium text-md bg-gray-100 p-2 rounded"
                    >
                      {servico} {servicoAberto === servico ? "▲" : "▼"}
                    </button>

                    {servicoAberto === servico && (
                      <ul className="ml-4 mt-2">
                        {grupos[mes][servico].map((disp) => (
                          <li key={disp.id} className="flex justify-between items-center p-2 border-b">
                            <span>
                              {new Date(disp.inicio).toLocaleString()} até {new Date(disp.final).toLocaleString()}
                            </span>
                            <button
                              onClick={() => handleDelete(disp.id)}
                              className="text-red-500 hover:text-red-700 transition"
                            >
                              <FaTrash size={18} />
                            </button>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Agenda;