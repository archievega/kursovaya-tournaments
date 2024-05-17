import { useState } from "react";
import securedFetch from './utils';

const CreateTournamentModal = ({ onClose, onCreate }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [startsAt, setStartsAt] = useState('');
    const [address, setAddress] = useState('');
    const [maxPlayers, setMaxPlayers] = useState(2);

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        const tournamentData = {
            title,
            description,
            starts_at: startsAt,
            address,
            max_players: maxPlayers
        };

        try {
            const response = await securedFetch('http://localhost:1234/api/v1/tournaments/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(tournamentData)
            });
            onCreate(response);  // Сообщаем родительскому компоненту о создании турнира
            onClose();  // Закрываем модальное окно
        } catch (error) {
            console.error('Error creating tournament:', error);
        }
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <span className="close" onClick={onClose}>&times;</span>
                <h2>Создать турнир</h2>
                <form onSubmit={handleSubmit}>
                    <label>
                        Название: 
                        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
                    </label>
                    <label>
                        Описание: 
                        <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} />
                    </label>
                    <label>
                        Дата начала: 
                        <input type="date" value={startsAt} onChange={(e) => setStartsAt(e.target.value)} required />
                    </label>
                    <label>
                        Адрес: 
                        <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} required />
                    </label>
                    <label>
                        Макс. игроков: 
                        <input type="number" value={maxPlayers} onChange={(e) => setMaxPlayers(e.target.value)} required />
                    </label>
                    <button type="submit">Создать</button>
                </form>
            </div>
        </div>
    );
};

export default CreateTournamentModal;
