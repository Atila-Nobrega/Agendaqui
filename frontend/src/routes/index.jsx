import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import CadastrarServico from "../pages/CadastrarServico";
import EscolherRole from "../pages/EscolherRole";
import Layout from "../layouts/Layout";
import Agenda from "../pages/Agenda";
import Calendario from "../pages/Calendario";

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout> <Login /> </Layout>} />
        <Route path="/agenda" element={<Layout><Agenda /></Layout>} />
        <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
        <Route path="/cadastrar-servico" element={<Layout><CadastrarServico /></Layout>} />
        <Route path="/escolher-role" element={<EscolherRole />} />
        <Route path="/calendario/:email" element={<Layout><Calendario /></Layout>} /> 
      </Routes>
    </Router>
  );
};

export default AppRoutes;