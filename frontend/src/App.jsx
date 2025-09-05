import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { CssVarsProvider, Sheet, Typography, Button} from "@mui/joy";

// Import your pages
import UploadPage from './pages/UploadPage'
import Chat from './pages/Chat'
import Load from './pages/Load'
import Mapping from './pages/Mapping'
import Validation from './pages/Validation'

function App() {

  return (
    <CssVarsProvider>
      <Router>
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/mapping" element={<Mapping />} />
          <Route path="/load" element={<Load />} />
          <Route path="/validation" element={<Validation />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </Router>
    </CssVarsProvider>
  )
}

export default App
