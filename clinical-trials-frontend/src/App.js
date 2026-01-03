import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,
  Typography, Box, Container, LinearProgress, Alert, useMediaQuery
} from '@mui/material';
import { useTheme } from '@mui/material/styles';

function App() {
  const [trials, setTrials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));

  useEffect(() => {
    axios.get('http://localhost:8000/api/trials/')
      .then(response => {
        setTrials(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.log('Error fetching data:', error);
        setError('Failed to load trials data');
        setLoading(false);
      });
  }, []);

  // Responsive column configuration
  const getVisibleColumns = () => {
    if (isMobile) return ['trial_id', 'title']; // Only show 2 columns on mobile
    if (isTablet) return ['trial_id', 'title', 'recruitment_status']; // 3 columns on tablet
    return ['trial_id', 'title', 'recruitment_status', 'health_condition', 'locations']; // All columns on desktop
  };

  const visibleColumns = getVisibleColumns();

  // Column headers mapping
  const columnHeaders = {
    trial_id: 'CTRI No.',
    title: 'Public Title',
    recruitment_status: 'Recruitment Status',
    health_condition: 'Health Condition',
    locations: 'Location'
  };

  // Function to truncate text for mobile
  const truncateText = (text, length) => {
    if (isMobile && text && text.length > length) {
      return text.substring(0, length) + '...';
    }
    return text;
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <LinearProgress />
        <Typography variant="h6" align="center" sx={{ mt: 2 }}>
          Loading clinical trials data...
        </Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: isMobile ? 2 : 4 }}>
      <Box sx={{ mb: isMobile ? 2 : 4 }}>
        <Typography 
          variant={isMobile ? "h5" : "h4"} 
          component="h1" 
          gutterBottom
          sx={{ fontWeight: 'bold', color: 'primary.main' }}
        >
          Clinical Trials Dashboard
        </Typography>
        <Typography 
          variant={isMobile ? "body2" : "subtitle1"} 
          color="text.secondary"
          gutterBottom
        >
          Showing {trials.length} clinical trials
        </Typography>
      </Box>

      <Paper 
        elevation={isMobile ? 1 : 3} 
        sx={{ 
          width: '100%',
          overflow: 'auto',
          maxHeight: isMobile ? '70vh' : '75vh'
        }}
      >
        <TableContainer>
          <Table 
            size={isMobile ? "small" : "medium"}
            stickyHeader
            aria-label="clinical trials table"
          >
            <TableHead>
              <TableRow>
                {visibleColumns.map(column => (
                  <TableCell 
                    key={column}
                    sx={{ 
                      fontWeight: 'bold',
                      backgroundColor: 'primary.light',
                      color: 'white',
                      fontSize: isMobile ? '0.75rem' : '0.875rem'
                    }}
                  >
                    {columnHeaders[column]}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {trials.map(trial => (
                <TableRow 
                  key={trial.id}
                  sx={{ 
                    '&:hover': { backgroundColor: 'action.hover' },
                    '&:nth-of-type(odd)': { backgroundColor: 'action.hover' }
                  }}
                >
                  {visibleColumns.map(column => (
                    <TableCell 
                      key={column}
                      sx={{ 
                        fontSize: isMobile ? '0.75rem' : '0.875rem',
                        py: isMobile ? 1 : 1.5
                      }}
                    >
                      {truncateText(trial[column], isMobile ? 30 : 60)}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Responsive footer */}
      <Box sx={{ 
        mt: isMobile ? 1 : 2, 
        display: 'flex', 
        justifyContent: 'space-between',
        flexDirection: isMobile ? 'column' : 'row',
        gap: isMobile ? 1 : 0
      }}>
        <Typography 
          variant="caption" 
          color="text.secondary"
          sx={{ fontSize: isMobile ? '0.7rem' : '0.75rem' }}
        >
          Data sourced from Clinical Trials Registry - India (CTRI)
        </Typography>
        <Typography 
          variant="caption" 
          color="text.secondary"
          sx={{ fontSize: isMobile ? '0.7rem' : '0.75rem' }}
        >
          Last updated: {new Date().toLocaleDateString()}
        </Typography>
      </Box>
    </Container>
  );
}

export default App;