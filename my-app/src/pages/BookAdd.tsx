import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import {
  Container,
  TextField,
  Button,
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  IconButton,
  Grid,
} from "@mui/material";
import { Autocomplete } from "@mui/lab";
import axios from "axios";
import { Author } from "../interfaces/Author";
import { Buyer } from "../interfaces/Buyer";
import { Publisher } from "../interfaces/Publisher";
import { BASE_URL } from "../common/constants";
import { Link, useNavigate, useParams } from "react-router-dom";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

interface BookForm {
  title: string;
  number_of_pages: number;
  publish_date: string;
  quantity: number;
  ibn: number;
  price: number;
  author: string;
  publisher: string;
  buyers: string[];
}

const BookAdd = () => {
  const { register, handleSubmit, setValue, formState: { errors } } = useForm<BookForm>({
    defaultValues: {
      title: "",
      number_of_pages: 0,
      publish_date: "",
      ibn: 0,
      price: 0,
      quantity: 0,
      author: "",
      publisher: "",
      buyers: [],
    },
  });
  const [buyers, setBuyers] = useState<Buyer[]>([]);
  const [authors, setAuthors] = useState<Author[]>([]);
  const [publishers, setPublishers] = useState<Publisher[]>([]);
  const [loadingData, setLoadingData] = useState(true);
  const [authorPage, setAuthorPage] = useState(1);
  const [publisherPage, setPublisherPage] = useState(1);
  const [buyerPage, setBuyerPage] = useState(1);
  const { bookId } = useParams();

  const navigate = useNavigate();

  // Fetch buyers, authors, and publishers data
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch authors, publishers, and buyers
        const [authorsResponse, publishersResponse, buyersResponse] =
          await Promise.all([
            axios.get(
              `${BASE_URL}/authors/pagination/?page=${authorPage}&per_page=30`
            ),
            axios.get(
              `${BASE_URL}/publishers/pagination/?page=${publisherPage}&per_page=30`
            ),
            axios.get(
              `${BASE_URL}/buyers/pagination/?page=${buyerPage}&per_page=30`
            ),
          ]);

        setAuthors(authorsResponse.data.authors);
        setPublishers(publishersResponse.data.publishers);
        setBuyers(buyersResponse.data.buyers);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoadingData(false);
      }
    };

    fetchData();
  }, [authorPage, publisherPage, buyerPage]); // Update when the page variables change

  const onClickFetchAuthors = () => {
    setAuthorPage((prevPage) => prevPage + 1); // Increment the page number
  };

  const onClickFetchPublishers = () => {
    setPublisherPage((prevPage) => prevPage + 1); // Increment the page number
  };

  const onClickFetchBuyers = () => {
    setBuyerPage((prevPage) => prevPage + 1); // Increment the page number
  };

  // Fetch existing book data if in edit mode
  useEffect(() => {
    const fetchBook = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/books/${bookId}`);
        const bookData = response.data;
        setValue("title", bookData.title);
        setValue("number_of_pages", bookData.number_of_pages);
        setValue("publish_date", bookData.publish_date);
        setValue("ibn", bookData.ibn);
        setValue("price", bookData.price);
        setValue("quantity", bookData.quantity);
        setValue("author", bookData.author.id);
        setValue("publisher", bookData.publisher.id);
        setValue(
          "buyers",
          bookData.buyers.map((buyer: any) => buyer.id)
        );
      } catch (error) {
        console.error("Error fetching book data:", error);
      } finally {
      }
    };

    if (bookId) {
      fetchBook();
    }
  }, [bookId, setValue]);

  const onSubmit = async (data: BookForm) => {
    try {
      if (bookId) {
        console.log(data);

        await axios.put(`${BASE_URL}/books/${bookId}/`, data);
        console.log(data);
        alert("Book successfully updated!");
      } else {
        await axios.post(`${BASE_URL}/books/`, data);
        alert("Book successfully added!");
      }
      navigate("/books");
    } catch (error) {
      console.error("Error adding/updating book:", error);
      alert("Failed to add/update book.");
    }
  };

  if (loadingData) {
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
    <Container maxWidth="sm" sx={{ marginBottom: "2rem" }}>
      <Box sx={{ margin: 4 }}>
        <IconButton component={Link} sx={{ mr: 3 }} to="/books">
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h4" align="center">
          {bookId ? "Update Book" : "Add Book"}
        </Typography>
        <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              {" "}
              {/* First column */}
              <TextField
                label="Title"
                fullWidth
                {...register("title", { required: "Title is required" })}
                sx={{ mt: 2 }}
                error={errors.title != null}
                helperText={errors.title?.message}
              />
              <TextField
                label="Number of Pages"
                fullWidth
                type="number"
                {...register("number_of_pages", {
                  required: "This is required",
                  min: 1,
                  max: 1000,
                })}
                sx={{ mt: 2 }}
                error={errors.number_of_pages != null}
                helperText={errors.number_of_pages?.message}
              />
              <TextField
                label="Publish Date"
                fullWidth
                type="date"
                InputLabelProps={{ shrink: true }}
                {...register("publish_date", { required: "This is required" })}
                sx={{ mt: 2 }}
                error={errors.publish_date != null}
                helperText={errors.publish_date?.message}
              />
              <TextField
                label="IBN"
                fullWidth
                type="number"
                {...register("ibn", { required: "This is required" })}
                sx={{ mt: 2 }}
                error={errors.ibn != null}
                helperText={errors.ibn?.message}
              />
              <TextField
                label="Price"
                fullWidth
                type="number"
                {...register("price", { required: "This is required" })}
                sx={{ mt: 2 }}
                error={errors.price != null}
                helperText={errors.price?.message}
              />
              <TextField
                label="Quantity"
                fullWidth
                type="number"
                {...register("quantity", { required: "This is required" })}
                sx={{ mt: 2 }}
                error={errors.quantity != null}
                helperText={errors.quantity?.message}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              {" "}
              {/* Second column */}
              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel id="author-label">Author</InputLabel>
                <Select
                  labelId="author-label"
                  {...register("author", { required: "Author is required" })}
                  label="Author"
                  error={errors.author != null}

                >
                  {authors.map((author) => (
                    <MenuItem key={author.id} value={author.id}>
                      {author.first_name} {author.last_name}
                    </MenuItem>
                  ))}
                </Select>
                {errors.author && (
                  <Typography variant="caption" color="error">
                    {errors.author.message}
                  </Typography>
                )}
              </FormControl>
              <Button
                variant="contained"
                color="secondary"
                onClick={onClickFetchAuthors}
                fullWidth
                sx={{ mt: 1 }}
              >
                Load other Authors
              </Button>
              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel id="publisher-label">Publisher</InputLabel>
                <Select
                  labelId="publisher-label"
                  {...register("publisher", { required: "Publisher is required!" })}
                  label="Publisher"
                  error={errors.publisher != null}

                >
                  {publishers.map((publisher) => (
                    <MenuItem key={publisher.id} value={publisher.id}>
                      {publisher.name}
                    </MenuItem>
                  ))}
                </Select>
                {errors.publisher && (
                  <Typography variant="caption" color="error">
                    {errors.publisher.message}
                  </Typography>
                )}
              </FormControl>
              <Button
                variant="contained"
                color="secondary"
                onClick={onClickFetchPublishers}
                fullWidth
                sx={{ mt: 1 }}
              >
                Load other Publishers
              </Button>
              <Autocomplete
                multiple                
                options={buyers}
                getOptionLabel={(option) => `${option.name}`}
                fullWidth
                {...register("buyers", { required: "You must select at least a buyer!" })}
                sx={{ mt: 2 }}
                onChange={(_, value) =>
                  setValue(
                    "buyers",
                    value.map((buyer) => buyer.id.toString())
                  )
                }
                renderInput={(params) => (
                  <TextField
                  
                    {...params}
                    label="Buyers"
                    placeholder="Select Buyers"
                  />
                )}
              />
              <Button
                variant="contained"
                color="secondary"
                onClick={onClickFetchBuyers}
                fullWidth
                sx={{ mt: 1 }}
              >
                Load other Buyers
              </Button>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                sx={{ my: 3 }}
              >
                {bookId ? "Update Book" : "Add Book"}{" "}
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default BookAdd;
