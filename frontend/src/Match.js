const Match = (s) => {
    s = s.s
    if (s.status == 'ENDED') {
        s.winner = s.winner.username
    }
    else {
        s.winner = "Еще не определен"
    }
    return (
        <>
                <tr className='match'>
                    <td>
                        <a href={'/tournaments/' + s.id} className="match-title">{s.title}</a>
                    </td>
                    <td>
                        <p className="match-address">Адрес: {s.address}</p>
                    </td>
                    <td>
                        <p className="match-status">Статус: {s.status}</p>
                    </td>
                    <td>
                        <p className="match-winner">Победитель: {s.winner}</p>
                    </td>
                </tr>
        </>
    )
}

export default Match