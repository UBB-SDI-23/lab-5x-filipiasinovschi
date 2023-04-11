import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CircularProgress,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import { Container } from "@mui/system";
import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { BASE_URL } from "../common/constants";
import EditIcon from "@mui/icons-material/Edit";
import DeleteForeverIcon from "@mui/icons-material/DeleteForever";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { Book } from "../interfaces/Book";
import axios, { AxiosError } from "axios";
import UpgradeIcon from "@mui/icons-material/Upgrade";

export const BookDetails = () => {
  const { bookId } = useParams();
  const [book, setBook] = useState<Book>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const isEditMode = location.pathname.includes("edit");


  useEffect(() => {
    const fetchBook = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`${BASE_URL}/books/${bookId}`);
        setBook(response.data);
      } catch (err) {
        if (axios.isAxiosError(err)) {
          setError(err.message);
        } else {
          setError("An unknown error occurred.");
        }
      } finally {
        setLoading(false);
      }
    };
    fetchBook();
  }, [bookId]);

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

  if (error) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <Typography variant="h6" color="error">
          Error: {error}
        </Typography>
      </Box>
    );
  }

  return (
    <Container>
      <Card>
        <CardContent>
          <IconButton component={Link} sx={{ mr: 3 }} to={`/books`}>
            <ArrowBackIcon />
          </IconButton>{" "}
          <Typography variant="h4">Book Details</Typography>
          <Typography>Book Title: {book?.title}</Typography>
          <Typography>Book Price: {book?.price}</Typography>
          <Typography>
            Book Author First Name: {book?.author.first_name}
          </Typography>
          <Typography>
            Book Author Last Name: {book?.author.last_name}
          </Typography>
          <Typography>Book Publisher Name: {book?.publisher.name}</Typography>
          <Typography>Book Buyers:</Typography>
          <List>
            {book?.buyers?.map((buyer) => (
              <ListItem key={buyer.id} alignItems="center">
                <ListItemText
                  primary={buyer.name}
                  primaryTypographyProps={{ align: "center" }}
                />
              </ListItem>
            ))}
          </List>
        </CardContent>
        <CardActions>
          <Box display="flex" justifyContent="center" width="100%">
            <IconButton
              component={Link}
              sx={{ mr: 4 }}
              to={`/books/${bookId}/edit`}
            >
              <EditIcon />
            </IconButton>

            <IconButton
              component={Link}
              sx={{ mr: 3 }}
              to={`/books/${bookId}/delete`}
            >
              <DeleteForeverIcon sx={{ color: "red" }} />
            </IconButton>
          </Box>
        </CardActions>
      </Card>
    </Container>
  );
};
