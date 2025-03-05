import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

const Layout = ({ children }) => {
  return (
    <div className="flex h-screen w-screen bg-gray-100">
      <aside className="w-32 h-full bg-white shadow-lg">
        <Sidebar />
      </aside>

      <div className="flex flex-col flex-1">
        <header className="w-full bg-white shadow-md flex items-center">
          <Navbar />
        </header>
        
        <main className="flex-1 p-8 mx-auto w-screen max-w-8xl bg-white shadow">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;