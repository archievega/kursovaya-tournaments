import { parseISO, format } from 'date-fns';


const TournamentComponent = (s) => {

    const formatDateTime = (dateTime) => {
        const parsedDate = parseISO(dateTime);
        return format(parsedDate, 'HH:mm dd.MM.yyyy');
    };

    s = s.s
    if (s.status === 'ENDED') {
        s.winner = s.winner.username
    }
    else {
        s.winner = "Еще не определен"
    }
    return (
        <>
                <tr className='tournament'>
                    <td>
                        <a href={'/tournaments/' + s.id} className="tournament-title">{s.title}</a>
                    </td>
                    <td>
                        <p className="tournament-address">{s.address}</p>
                    </td>
                    <td>
                        <p className="tournament-date">{formatDateTime(s.starts_at)}</p>
                    </td>
                    <td>
                        <p className="tournament-winner">{s.winner}</p>
                    </td>
                    <td>
                        <p className="tournament-status">{s.status}</p>
                    </td>
                </tr>
        </>
    )
}

export default TournamentComponent