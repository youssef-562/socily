import React, { useState, useEffect } from 'react';
import {
    Box,
    Paper,
    Typography,
    CircularProgress,
    Chip,
    Grid,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import axios from 'axios';

const Alerts = () => {
        const [loading, setLoading] = useState(true);
        const [alerts, setAlerts] = useState([]);
        const [stats, setStats] = useState(null);

        useEffect(() => {
            const fetchData = async() => {
                try {
                    const [alertsRes, statsRes] = await Promise.all([
                        axios.get('/api/alerts'),
                        axios.get('/api/alerts/stats'),
                    ]);

                    setAlerts(alertsRes.data);
                    setStats(statsRes.data);
                } catch (error) {
                    console.error('Erreur lors du chargement des données:', error);
                } finally {
                    setLoading(false);
                }
            };

            fetchData();
        }, []);

        const getSeverityColor = (severity) => {
            switch (severity.toLowerCase()) {
                case 'critical':
                    return 'error';
                case 'high':
                    return 'warning';
                case 'medium':
                    return 'info';
                case 'low':
                    return 'success';
                default:
                    return 'default';
            }
        };

        const columns = [
            { field: 'id', headerName: 'ID', width: 90 },
            { field: 'title', headerName: 'Titre', width: 200 },
            {
                field: 'severity',
                headerName: 'Sévérité',
                width: 130,
                renderCell: (params) => ( <
                    Chip label = { params.value }
                    color = { getSeverityColor(params.value) }
                    />
                ),
            },
            { field: 'source', headerName: 'Source', width: 150 },
            {
                field: 'status',
                headerName: 'Statut',
                width: 130,
                renderCell: (params) => ( <
                    Chip label = { params.value }
                    color = {
                        params.value === 'RESOLVED' ?
                        'success' : params.value === 'IN_PROGRESS' ?
                            'warning' : 'default'
                    }
                    />
                ),
            },
            {
                field: 'tags',
                headerName: 'Tags',
                width: 200,
                renderCell: (params) => ( <
                    Box sx = {
                        { display: 'flex', gap: 0.5 }
                    } > {
                        params.value.map((tag) => ( <
                            Chip key = { tag }
                            label = { tag }
                            size = "small" / >
                        ))
                    } <
                    /Box>
                ),
            },
            {
                field: 'created_at',
                headerName: 'Créé le',
                width: 180,
                valueFormatter: (params) =>
                    new Date(params.value).toLocaleString(),
            },
            {
                field: 'updated_at',
                headerName: 'Mis à jour le',
                width: 180,
                valueFormatter: (params) =>
                    new Date(params.value).toLocaleString(),
            },
        ];

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

        return ( <
                Box >
                <
                Typography variant = "h4"
                gutterBottom >
                Alertes <
                /Typography>

                { /* Statistiques */ } <
                Grid container spacing = { 3 }
                sx = {
                    { mb: 4 }
                } >
                <
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
                /Typography> {
                stats ? .by_severity &&
                Object.entries(stats.by_severity).map(([severity, count]) => ( <
                    Box key = { severity }
                    sx = {
                        { mb: 1 }
                    } >
                    <
                    Typography variant = "body2" > { severity }: { count } <
                    /Typography> < /
                    Box >
                ))
            } <
            /Paper> < /
            Grid > <
            Grid item xs = { 12 }
        md = { 4 } >
            <
            Paper sx = {
                { p: 2 }
            } >
            <
            Typography variant = "h6"
        gutterBottom >
            Alertes par source <
            /Typography> {
        stats ? .by_source &&
            Object.entries(stats.by_source).map(([source, count]) => ( <
                Box key = { source }
                sx = {
                    { mb: 1 }
                } >
                <
                Typography variant = "body2" > { source }: { count } <
                /Typography> < /
                Box >
            ))
    } <
    /Paper> < /
    Grid > <
    /Grid>

{ /* Tableau des alertes */ } <
Paper sx = {
        { height: 600, width: '100%' }
    } >
    <
    DataGrid rows = { alerts }
columns = { columns }
pageSize = { 10 }
rowsPerPageOptions = {
    [10]
}
checkboxSelection disableSelectionOnClick /
    >
    <
    /Paper> < /
    Box >
);
};

export default Alerts;