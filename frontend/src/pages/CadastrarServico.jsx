import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { FaTrash } from "react-icons/fa";
import axios from "axios";

const CadastrarServico = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [servicos, setServicos] = useState([]);
  const [form, setForm] = useState({
    nome: "",
    descricao: "",
    preco: "",
  });

  useEffect(() => {
    if (user?.role !== "prestador") {
      navigate("/dashboard");
    } else {
      carregarServicos();
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

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      await axios.post("http://localhost:8000/servicos", form, {
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      });
      setForm({ nome: "", descricao: "", preco: "" });
      carregarServicos();
    } catch (error) {
      console.error("Erro ao cadastrar serviço", error);
    }
  };

  const handleDeleteServico = async (id) => {
    try {
      const token = localStorage.getItem("token");
  
      await axios.delete(`http://localhost:8000/servicos/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
  
      setServicos(servicos.filter((servico) => servico.id !== id));
    } catch (error) {
      console.error("Erro ao excluir serviço", error);
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto bg-white shadow-md rounded-md">
      <h1 className="text-2xl font-bold mb-4">Cadastrar Serviço</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="nome"
          placeholder="Nome do Serviço"
          value={form.nome}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        <textarea
          name="descricao"
          placeholder="Descrição"
          value={form.descricao}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        <input
          type="number"
          name="preco"
          placeholder="Preço (R$)"
          value={form.preco}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded"
          required
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Cadastrar Serviço
        </button>
      </form>

      <h2 className="text-xl font-semibold mt-6">Seus Serviços</h2>
      <ul className="mt-2">
        {servicos.map((servico) => (
          <li key={servico.id} className="p-2 border-b">
            <span className="font-medium">{servico.nome}</span> - R$ {servico.preco}
            <button onClick={() => handleDeleteServico(servico.id)} className="text-red-500 hover:text-red-700 transition"> <FaTrash size={18} /></button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CadastrarServico;