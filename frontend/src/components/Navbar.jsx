import logo from "../assets/logo.png";

const Navbar = () => {
    return (
      <nav className="flex items-center w-screen bg-blue-600 text-white">
        <img src={logo} alt="Logo" className="h-14 mr-3" />
        <h1 className="text-3xl">Agendaqui</h1>
      </nav>
    );
  };
  
  export default Navbar;