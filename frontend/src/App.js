import './App.css';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Registration from './Registration';
import Login from './Login';
import Home from './Home';
import Tournament from './Tournament';
import TournamentPlayers from './TournamentPlayers';
import { useEffect } from 'react';
// import { useState, useEffect } from 'react';
// import { createClient } from '@supabase/supabase-js';
// import { Auth } from '@supabase/auth-ui-react';
// import { ThemeSupa } from '@supabase/auth-ui-shared';
// const url = 'http://213.171.3.136/api/v1/auth/register'


// const supabase = createClient('http://213.171.3.136:8000', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE')
function App() {

  // console.log(supabase)
  // const [session, setSession] = useState()
  // useEffect(() => {
  //   supabase.auth.getSession().then(({ data: { session } }) => {
  //     setSession(session)
  //   })
  //   const {
  //     data: { subscription },
  //   } = supabase.auth.onAuthStateChange((_event, session) => {
  //     setSession(session)
  //   })
  //   return () => subscription.unsubscribe()
  // }, [])
  // console.log(session, 'sadsa')
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registration" element={<Registration />} />
        <Route path="/tournaments" element={<Home />} />
        <Route path="/tournaments/:tournamentId" element={<Tournament />} />
        <Route path="/tournaments/:tournamentId/players" element={<TournamentPlayers />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
