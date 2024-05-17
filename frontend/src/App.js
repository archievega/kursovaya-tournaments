import './App.css';
import { Route, Routes, BrowserRouter, Navigate } from 'react-router-dom';
import Registration from './Registration';
import Login from './Login';
import Home from './Home';
import Tournament from './Tournament';
import NotFound from './NotFound';
import TournamentMatches from './TournamentMatches';
import Leaderboard from './Leaderboard';


const App = () => {
  const token = localStorage.getItem('token');

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={token ? <Navigate replace to="/tournaments" /> : <Navigate replace to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registration" element={<Registration />} />
        <Route path="/tournaments" element={<Home />} />
        <Route path="/tournaments/:tournamentId" element={<Tournament />} />
        <Route path="/tournaments/:tournamentId/matches" element={<TournamentMatches />} />
        <Route path="/not-found" element={<NotFound />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
