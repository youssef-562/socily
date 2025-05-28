import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

// Composants
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Actions from './pages/Actions';
import Alerts from './pages/Alerts';
import Analyses from './pages/Analyses';

// Thème personnalisé
const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#2196f3',
        },
        secondary: {
            main: '#f50057',
        },
        background: {
            default: '#121212',
            paper: '#1e1e1e',
        },
    },
});

function App() {
    return ( <
        ThemeProvider theme = { theme } >
        <
        CssBaseline / >
        <
        Router >
        <
        Box sx = {
            { display: 'flex', flexDirection: 'column', minHeight: '100vh' }
        } >
        <
        Navbar / >
        <
        Box component = "main"
        sx = {
            { flexGrow: 1, p: 3 }
        } >
        <
        Routes >
        <
        Route path = "/"
        element = { < Dashboard / > }
        /> <
        Route path = "/actions"
        element = { < Actions / > }
        /> <
        Route path = "/alerts"
        element = { < Alerts / > }
        /> <
        Route path = "/analyses"
        element = { < Analyses / > }
        /> < /
        Routes > <
        /Box> < /
        Box > <
        /Router> < /
        ThemeProvider >
    );
}

export default App;