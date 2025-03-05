const Login = () => {
  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:8000/auth/google";
  };

  return (
    <div>
      <div className="bg-white p-8 rounded-lg shadow-lg text-center">
        <h1 className="text-2xl font-bold mb-4">Bem-vindo ao Agendaqui</h1>
        <p className="mb-4 text-gray-600">Faça login com sua conta Google</p>
        <button
          onClick={handleGoogleLogin}
          className="bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition"
        >
          Login com Google
        </button>
      </div>
    </div>
  );
};

export default Login;