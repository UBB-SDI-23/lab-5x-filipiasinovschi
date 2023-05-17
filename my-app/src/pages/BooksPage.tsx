import React,{ useEffect, useState } from "react";
import {
  Box,
  Button,
  CircularProgress,
  Container,
  IconButton,
  InputLabel,
  Pagination,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import { Book } from "../interfaces/Book";
import { BASE_URL } from "../common/constants";
import { Link } from "react-router-dom";
import { Add, DeleteForever, Edit, NumbersRounded, ReadMore } from "@mui/icons-material";

const BooksPage = () => {
  const [loading, setLoading] = useState(false);
  const [books, setBooks] = useState<Book[]>();
  const [minPages, setMinPages] = useState<number>();
  const [currentPage, setCurrentPage] = useState(1); // Added state for current page
  const [totalPages, setTotalPages] = useState(0); // Added state for total pages

  const handlePageChange = (event: React.ChangeEvent<unknown>, page: number) => {
    setCurrentPage(page);
  };
  
  // Inside the fetchBooks() function, update the URL to include the current page parameter
  const fetchBooks = () => {
    setLoading(true);
    fetch(`${BASE_URL}/books/pagination/?page=${currentPage}&per_page=10`) // Updated API endpoint with pagination parameters
      .then((response) => response.json())
      .then((data) => {
        setBooks(data.books);
        setTotalPages(Math.floor(data.total_count/10));
        setLoading(false);
      });
  };
  useEffect(() => {
    fetchBooks();
  }, [currentPage]);

  
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMinPages(parseInt(event.target.value));
  };

  const handleFilter = () => {
    if (!minPages || minPages === 0) {
      fetchBooks();
    } else if (minPages > 0) {
      setLoading(true);
      fetch(`${BASE_URL}/books/above/${minPages}/`)
        .then((response) => response.json())
        .then((data) => {
          setBooks(data);
          setLoading(false);
        });
    }
  };

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }


  return (
    <Container maxWidth="xl">
      <Box mt={4} mb={2}>
        <Typography variant="h4" component="h1">
          Books List
        </Typography>
      </Box>
      {!loading && (
        <IconButton component={Link} sx={{ mr: 3 }} to={`/books/add`}>
          <Tooltip title="Add a new book" arrow>
            <Add color="primary" />
          </Tooltip>
        </IconButton>
      )}
      <Box mb={2} display="flex" alignItems="center" gap="1rem" justifyContent="right">
        <InputLabel htmlFor="min-pages">Books with pages above</InputLabel>
        <TextField
          id="min-pages"
          type="number"
          value={minPages}
          onChange={handleChange}
        />
        <Button
          onClick={handleFilter}
          variant="contained"
          color="primary"
          sx={{ ml: 2 }}
        >
          Filter
        </Button>
      </Box>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell align="right">#</TableCell>
              <TableCell align="right">Title</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell align="right">Pages</TableCell>
              <TableCell align="right">Quantity</TableCell>
              <TableCell align="right">No. Buyers</TableCell>
              <TableCell align="right">Operations</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {books &&
              books.map((book, idx) => {
                return (
                  <TableRow key={idx}>
                    <TableCell align="right">{idx + 1}</TableCell>
                    <TableCell align="right">{book.title}</TableCell>
                    <TableCell align="right">{book.price}</TableCell>
                    <TableCell align="right">{book.number_of_pages}</TableCell>
                    <TableCell align="right">{book.quantity}</TableCell>
                    <TableCell align="right">{book.buyers.length}</TableCell>

                    <TableCell align="right">
                      <IconButton
                        component={Link}
                        sx={{ mr: 3 }}
                        to={`/books/${book.id}/details`}
                      >
                        <Tooltip title="View course details" arrow>
                          <ReadMore color="primary" />
                        </Tooltip>
                      </IconButton>

                      <IconButton
                        component={Link}
                        sx={{ mr: 3 }}
                        to={`/books/${book.id}/edit`}
                      >
                        <Edit />
                      </IconButton>

                      <IconButton
                        component={Link}
                        to={`/books/${book.id}/delete`}
                      >
                        <DeleteForever sx={{ color: "red" }} />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
      <Box display="flex" justifyContent="center" mt={2} mb={2}>
      <Pagination
        count={totalPages}
        page={currentPage}
        onChange={handlePageChange}
        color="primary"
        shape="rounded"
      />
    </Box>
    </Container>
  );
};

export default BooksPage;
