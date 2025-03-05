import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import LogoutButton from "../components/LogoutButton";

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("access_token");

    if (token) {
      localStorage.setItem("token", token);
      navigate("/dashboard", { replace: true });
    } else {
      const storedToken = localStorage.getItem("token");
      if (!storedToken) {
        navigate("/");
      }
    }

    if (user?.role === "user") {
        navigate("/escolher-role");
    }

  }, [user, navigate]);

  return (
    <div>
      <h1>Dashboard</h1>
      {user ? (
        <>
          <img src={`${user.picture}`}
               className="w-20 h-20 rounded-full shadow-lg"></img>
          <p>Bem-vindo, <strong>{user.name}</strong>!</p>
          <p>Email: {user.email}</p>
          <p>Tipo de conta: <strong>{user.role}</strong></p>
          <LogoutButton />
        </>
      ) : (
        <p>Carregando...</p>
      )}
    </div>
  );
};

export default Dashboard;