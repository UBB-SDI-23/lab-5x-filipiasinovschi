import { useState } from 'react'
import './App.css'
import { Route, Routes, BrowserRouter as Router } from 'react-router-dom'
import BooksPage from './pages/BooksPage'
import { AppMenu } from './components/AppMenu'
import { AppHome } from './pages/AppHome'
import { BookDelete } from './pages/BookDelete'
import { BookDetails } from './pages/BookDetails'
import BookAdd from './pages/BookAdd'
function App() {

  return (
    <div className="App">

      <Router>
        <AppMenu />

        <Routes>
          <Route path="/" element={<AppHome />} />
          <Route path="/books" element={<BooksPage />} />
          <Route path="/books/:bookId/details" element={<BookDetails />} />
					<Route path="/books/:bookId/edit" element={<BookAdd />} />
					<Route path="/books/add" element={< BookAdd/>} />
          <Route path="/books/:bookId/delete" element={<BookDelete />} />

        </Routes>
      </Router>

    </div>
  )
}

export default App
