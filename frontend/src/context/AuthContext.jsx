import { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    
    if (token) {
      const payload = JSON.parse(atob(token.split(".")[1]));
      setUser({ 
        id: payload.id,
        name: payload.name,
        picture: payload.picture,
        email: payload.email, 
        role: payload.role
      });
    }

    setLoading(false);
  }, []);

  const login = (token) => {
    localStorage.setItem("token", token);
    const payload = JSON.parse(atob(token.split(".")[1]));
    setUser({ 
        id: payload.id,
        name: payload.name,
        picture: payload.picture,
        email: payload.email, 
        role: payload.role
    });
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);