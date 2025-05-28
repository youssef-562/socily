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

const Actions = () => {
        const [loading, setLoading] = useState(true);
        const [actions, setActions] = useState([]);
        const [stats, setStats] = useState(null);

        useEffect(() => {
            const fetchData = async() => {
                try {
                    const [actionsRes, statsRes] = await Promise.all([
                        axios.get('/api/actions'),
                        axios.get('/api/actions/stats'),
                    ]);

                    setActions(actionsRes.data);
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
            { field: 'type', headerName: 'Type', width: 150 },
            {
                field: 'status',
                headerName: 'Statut',
                width: 130,
                renderCell: (params) => ( <
                    Chip label = { params.value }
                    color = {
                        params.value === 'COMPLETED' ?
                        'success' : params.value === 'FAILED' ?
                            'error' : params.value === 'IN_PROGRESS' ?
                            'warning' : 'default'
                    }
                    />
                ),
            },
            {
                field: 'parameters',
                headerName: 'Paramètres',
                width: 200,
                renderCell: (params) => ( <
                    Typography variant = "body2" > { JSON.stringify(params.value) } <
                    /Typography>
                ),
            },
            {
                field: 'result',
                headerName: 'Résultat',
                width: 200,
                renderCell: (params) => ( <
                    Typography variant = "body2" > { params.value ? JSON.stringify(params.value) : '-' } <
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
                Actions <
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
                Actions par type <
                /Typography> {
                stats ? .by_type &&
                Object.entries(stats.by_type).map(([type, count]) => ( <
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
            Grid item xs = { 12 }
        md = { 4 } >
            <
            Paper sx = {
                { p: 2 }
            } >
            <
            Typography variant = "h6"
        gutterBottom >
            Actions par statut <
            /Typography> {
        stats ? .by_status &&
            Object.entries(stats.by_status).map(([status, count]) => ( <
                Box key = { status }
                sx = {
                    { mb: 1 }
                } >
                <
                Typography variant = "body2" > { status }: { count } <
                /Typography> < /
                Box >
            ))
    } <
    /Paper> < /
Grid > <
    /Grid>

{ /* Tableau des actions */ } <
Paper sx = {
        { height: 600, width: '100%' }
    } >
    <
    DataGrid rows = { actions }
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

export default Actions;