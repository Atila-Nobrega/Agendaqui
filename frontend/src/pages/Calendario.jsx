import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const coresServicos = [
    "#1982C4", "#6A4C93", "#8AC926", "#FFCA3A", "#f49cbb", "#b8e0d2", "#cae9ff"
];

const mapaCores = {};

const Calendario = () => {
    const { email } = useParams();
    const [disponibilidades, setDisponibilidades] = useState([]);
    const [eventoSelecionado, setEventoSelecionado] = useState(null);

    useEffect(() => {
        const carregarDisponibilidades = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/disponibilidade/prestador`, {
                    params: { email }
                });

                const eventos = response.data.map((disp) => {
                    if (!mapaCores[disp.servico_nome]) {
                        mapaCores[disp.servico_nome] = coresServicos[Object.keys(mapaCores).length % coresServicos.length];
                    }
                    return {
                        id: disp.id,
                        title: disp.servico_nome,
                        start: disp.inicio,
                        end: disp.final,
                        backgroundColor: mapaCores[disp.servico_nome],
                        borderColor: "#fff",
                    };
                });

                setDisponibilidades(eventos);
            } catch (error) {
                console.error("Erro ao carregar disponibilidades:", error);
            }
        };

        carregarDisponibilidades();
    }, [email]);

    const handleEventClick = (clickInfo) => {
        setEventoSelecionado(clickInfo.event);
    };

    const fecharModal = () => {
        setEventoSelecionado(null);
    };

    return (
        <div className="p-6 max-w-6xl mx-auto bg-white shadow-md rounded-md">
            <h1 className="text-2xl font-bold mb-4">Calendário de Disponibilidades</h1>
            <p className="text-gray-600">Mostrando disponibilidades para: <strong>{email}</strong></p>

            <FullCalendar
                plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
                initialView="timeGridWeek"
                events={disponibilidades}
                headerToolbar={{
                    left: "prev,next today",
                    center: "title",
                    right: "dayGridMonth,timeGridWeek,timeGridDay"
                }}
                height="auto"
                eventClick={handleEventClick}
            />

            {eventoSelecionado && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
                    <div className="bg-white p-6 rounded shadow-lg w-96 relative z-50">
                        <button
                            onClick={fecharModal}
                            className="absolute top-2 right-2 text-gray-600 hover:text-gray-800"
                        >
                            ✖
                        </button>
                        <h2 className="text-xl font-bold">{eventoSelecionado.title}</h2>
                        <p className="mt-2 text-gray-600">
                            <strong>Início:</strong> {new Date(eventoSelecionado.start).toLocaleString()} <br />
                            <strong>Fim:</strong> {new Date(eventoSelecionado.end).toLocaleString()}
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Calendario;