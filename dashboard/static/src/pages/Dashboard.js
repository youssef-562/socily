import React, { useState, useEffect } from 'react';
import {
    Grid,
    Paper,
    Typography,
    Box,
    CircularProgress,
} from '@mui/material';
import { Line, Pie } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
} from 'chart.js';
import axios from 'axios';

// Enregistrement des composants Chart.js
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

const Dashboard = () => {
        const [loading, setLoading] = useState(true);
        const [summary, setSummary] = useState(null);
        const [actionStats, setActionStats] = useState(null);
        const [alertStats, setAlertStats] = useState(null);

        useEffect(() => {
            const fetchData = async() => {
                try {
                    const [summaryRes, actionStatsRes, alertStatsRes] = await Promise.all([
                        axios.get('/api/dashboard/summary'),
                        axios.get('/api/actions/stats'),
                        axios.get('/api/alerts/stats'),
                    ]);

                    setSummary(summaryRes.data);
                    setActionStats(actionStatsRes.data);
                    setAlertStats(alertStatsRes.data);
                } catch (error) {
                    console.error('Erreur lors du chargement des données:', error);
                } finally {
                    setLoading(false);
                }
            };

            fetchData();
        }, []);

        if (loading) {
            return ( <
                Box display = "flex"
                justifyContent = "center"
                alignItems = "center"
                minHeight = "80vh" >
                <
                CircularProgress / >
                <
                /Box>
            );
        }

        // Configuration des graphiques
        const actionChartData = {
            labels: Object.keys(actionStats ? .by_day || {}),
            datasets: [{
                label: 'Actions par jour',
                data: Object.values(actionStats ? .by_day || {}),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
            }, ],
        };

        const alertChartData = {
            labels: Object.keys(alertStats ? .by_severity || {}),
            datasets: [{
                data: Object.values(alertStats ? .by_severity || {}),
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 206, 86)',
                    'rgb(75, 192, 192)',
                ],
            }, ],
        };

        return ( <
                Box >
                <
                Typography variant = "h4"
                gutterBottom >
                Tableau de bord <
                /Typography>

                { /* Statistiques globales */ } <
                Grid container spacing = { 3 }
                sx = {
                    { mb: 4 }
                } >
                <
                Grid item xs = { 12 }
                sm = { 6 }
                md = { 3 } >
                <
                Paper sx = {
                    { p: 2, textAlign: 'center' }
                } >
                <
                Typography variant = "h6" > Actions totales < /Typography> <
                Typography variant = "h4" > { summary ? .total_actions } < /Typography> < /
                Paper > <
                /Grid> <
                Grid item xs = { 12 }
                sm = { 6 }
                md = { 3 } >
                <
                Paper sx = {
                    { p: 2, textAlign: 'center' }
                } >
                <
                Typography variant = "h6" > Alertes totales < /Typography> <
                Typography variant = "h4" > { summary ? .total_alerts } < /Typography> < /
                Paper > <
                /Grid> <
                Grid item xs = { 12 }
                sm = { 6 }
                md = { 3 } >
                <
                Paper sx = {
                    { p: 2, textAlign: 'center' }
                } >
                <
                Typography variant = "h6" > Analyses totales < /Typography> <
                Typography variant = "h4" > { summary ? .total_analyses } < /Typography> < /
                Paper > <
                /Grid> <
                Grid item xs = { 12 }
                sm = { 6 }
                md = { 3 } >
                <
                Paper sx = {
                    { p: 2, textAlign: 'center' }
                } >
                <
                Typography variant = "h6" > Actions en cours < /Typography> <
                Typography variant = "h4" > { summary ? .pending_actions } < /Typography> < /
                Paper > <
                /Grid> < /
                Grid >

                { /* Graphiques */ } <
                Grid container spacing = { 3 } >
                <
                Grid item xs = { 12 }
                md = { 8 } >
                <
                Paper sx = {
                    { p: 2 }
                } >
                <
                Typography variant = "h6"
                gutterBottom >
                Évolution des actions <
                /Typography> <
                Line data = { actionChartData }
                /> < /
                Paper > <
                /Grid> <
                Grid item xs = { 12 }
                md = { 4 } >
                <
                Paper sx = {
                    { p: 2 }
                } >
                <
                Typography variant = "h6"
                gutterBottom >
                Alertes par sévérité <
                /Typography> <
                Pie data = { alertChartData }
                /> < /
                Paper > <
                /Grid> < /
                Grid >

                { /* Actions et alertes récentes */ } <
                Grid container spacing = { 3 }
                sx = {
                    { mt: 3 }
                } >
                <
                Grid item xs = { 12 }
                md = { 6 } >
                <
                Paper sx = {
                    { p: 2 }
                } >
                <
                Typography variant = "h6"
                gutterBottom >
                Actions récentes <
                /Typography> {
                summary ? .recent_actions.map((action) => ( <
                    Box key = { action.id }
                    sx = {
                        { mb: 1 }
                    } >
                    <
                    Typography variant = "body2" > { action.type } - { action.status } <
                    /Typography> < /
                    Box >
                ))
            } <
            /Paper> < /
            Grid > <
            Grid item xs = { 12 }
        md = { 6 } >
            <
            Paper sx = {
                { p: 2 }
            } >
            <
            Typography variant = "h6"
        gutterBottom >
            Alertes récentes <
            /Typography> {
        summary ? .recent_alerts.map((alert) => ( <
            Box key = { alert.id }
            sx = {
                { mb: 1 }
            } >
            <
            Typography variant = "body2" > { alert.title } - { alert.severity } <
            /Typography> < /
            Box >
        ))
    } <
    /Paper> < /
    Grid > <
    /Grid> < /
    Box >
);
};

export default Dashboard;