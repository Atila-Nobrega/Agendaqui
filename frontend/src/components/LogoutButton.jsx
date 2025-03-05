import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const LogoutButton = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); // 🔹 Remove o token e reseta o estado do usuário
    navigate("/"); // 🔹 Redireciona para a página inicial
  };

  return (
    <button 
      onClick={handleLogout} 
      className="bg-red-500 text-white px-4 py-2 rounded-lg mt-4 hover:bg-red-600 transition"
    >
      Logout
    </button>
  );
};

export default LogoutButton;