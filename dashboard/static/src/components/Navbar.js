import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
    AppBar,
    Toolbar,
    Typography,
    Button,
    Box,
    IconButton,
} from '@mui/material';
import {
    Dashboard as DashboardIcon,
    Security as SecurityIcon,
    Warning as WarningIcon,
    Assessment as AssessmentIcon,
} from '@mui/icons-material';

const Navbar = () => {
    return ( <
        AppBar position = "static" >
        <
        Toolbar >
        <
        Typography variant = "h6"
        component = "div"
        sx = {
            { flexGrow: 1 }
        } >
        SOCily Dashboard <
        /Typography> <
        Box sx = {
            { display: 'flex', gap: 1 }
        } >
        <
        Button color = "inherit"
        component = { RouterLink }
        to = "/"
        startIcon = { < DashboardIcon / > } >
        Dashboard <
        /Button> <
        Button color = "inherit"
        component = { RouterLink }
        to = "/actions"
        startIcon = { < SecurityIcon / > } >
        Actions <
        /Button> <
        Button color = "inherit"
        component = { RouterLink }
        to = "/alerts"
        startIcon = { < WarningIcon / > } >
        Alertes <
        /Button> <
        Button color = "inherit"
        component = { RouterLink }
        to = "/analyses"
        startIcon = { < AssessmentIcon / > } >
        Analyses <
        /Button> < /
        Box > <
        /Toolbar> < /
        AppBar >
    );
};

export default Navbar;