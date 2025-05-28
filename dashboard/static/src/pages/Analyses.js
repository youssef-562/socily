import React, { useState, useEffect } from 'react';
import {
    Box,
    Paper,
    Typography,
    CircularProgress,
    Grid,
    Chip,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import axios from 'axios';

const Analyses = () => {
        const [loading, setLoading] = useState(true);
        const [analyses, setAnalyses] = useState([]);
        const [stats, setStats] = useState(null);

        useEffect(() => {
            const fetchData = async() => {
                try {
                    const [analysesRes, statsRes] = await Promise.all([
                        axios.get('/api/analyses'),
                        axios.get('/api/analyses/stats'),
                    ]);

                    setAnalyses(analysesRes.data);
                    setStats(statsRes.data);
                } catch (error) {
                    console.error('Erreur lors du chargement des données:', error);
                } finally {
                    setLoading(false);
                }
            };

            fetchData();
        }, []);

        const columns = [
            { field: 'id', headerName: 'ID', width: 90 },
            { field: 'source', headerName: 'Source', width: 150 },
            {
                field: 'timeframe',
                headerName: 'Période',
                width: 150,
                valueFormatter: (params) => {
                    const { start, end } = params.value;
                    return `${new Date(start).toLocaleString()} - ${new Date(end).toLocaleString()}`;
                },
            },
            {
                field: 'threats_detected',
                headerName: 'Menaces détectées',
                width: 200,
                renderCell: (params) => ( <
                    Box sx = {
                        { display: 'flex', gap: 0.5, flexWrap: 'wrap' }
                    } > {
                        params.value.map((threat, index) => ( <
                            Chip key = { index }
                            label = { threat.type }
                            color = {
                                threat.severity === 'high' ?
                                'error' : threat.severity === 'medium' ?
                                    'warning' : 'info'
                            }
                            size = "small" /
                            >
                        ))
                    } <
                    /Box>
                ),
            },
            {
                field: 'recommendations',
                headerName: 'Recommandations',
                width: 200,
                renderCell: (params) => ( <
                    Typography variant = "body2" > { params.value.join(', ') } <
                    /Typography>
                ),
            },
            {
                field: 'statistics',
                headerName: 'Statistiques',
                width: 200,
                renderCell: (params) => ( <
                    Typography variant = "body2" > { JSON.stringify(params.value) } <
                    /Typography>
                ),
            },
            {
                field: 'created_at',
                headerName: 'Créé le',
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
                Analyses de logs <
                /Typography>

                { /* Statistiques */ } <
                Grid container spacing = { 3 }
                sx = {
                    { mb: 4 }
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
                Analyses par source <
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
            Grid item xs = { 12 }
        md = { 6 } >
            <
            Paper sx = {
                { p: 2 }
            } >
            <
            Typography variant = "h6"
        gutterBottom >
            Menaces par type <
            /Typography> {
        stats ? .threats_by_type &&
            Object.entries(stats.threats_by_type).map(([type, count]) => ( <
                Box key = { type }
                sx = {
                    { mb: 1 }
                } >
                <
                Typography variant = "body2" > { type }: { count } <
                /Typography> < /
                Box >
            ))
    } <
    /Paper> < /
Grid > <
    /Grid>

{ /* Tableau des analyses */ } <
Paper sx = {
        { height: 600, width: '100%' }
    } >
    <
    DataGrid rows = { analyses }
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

export default Analyses;