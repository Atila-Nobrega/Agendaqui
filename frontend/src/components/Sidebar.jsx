import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <aside className="w-64 bg-gray-900 text-white h-screen p-4">
      <ul>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/cadastrar-servico">+Serviços</Link></li>
        <li><Link to="/agenda">Agenda</Link></li>
      </ul>
    </aside>
  );
};

export default Sidebar;