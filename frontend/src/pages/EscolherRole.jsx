import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const EscolherRole = () => {
  const { user, login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user?.role !== "user") {
      navigate("/dashboard");
    }
  }, [user, navigate]);

  const handleChooseRole = async (role) => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.post(
        "http://localhost:8000/user/update-role",
        { role },
        { 
          headers: { 
            Authorization: `Bearer ${token}`, 
            "Content-Type": "application/json"
          } 
        }
      );

      if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        login(response.data.access_token);
        navigate("/dashboard");
      }
    } catch (error) {
      console.error("Erro ao definir a role", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 w-screen">
      <h1 className="text-2xl font-bold mb-4">Escolha sua função</h1>
      <p className="mb-6">Para continuar, selecione se deseja ser Cliente ou Prestador.</p>
      <div className="flex gap-4">
        <button
          className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition"
          onClick={() => handleChooseRole("cliente")}
        >
          Quero ser Cliente
        </button>
        <button
          className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition"
          onClick={() => handleChooseRole("prestador")}
        >
          Quero ser Prestador
        </button>
      </div>
    </div>
  );
};

export default EscolherRole;