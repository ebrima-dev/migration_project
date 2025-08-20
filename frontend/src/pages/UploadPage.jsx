import React, { useState } from "react";
import { Button, Card, Typography, Box, Container } from "@mui/joy";

export default function UploadPage() {
    const [file, setFile] = useState(null); 
    const [status, setStatus] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            setStatus("Please select a file first.");
            return;
        }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://localhost:8000/upload-file/", {
            method: "POST",
            body: formData,
        });
        const data = await res.json();
        if (res.ok) {
            setStatus(`File uploaded: ${data.filename}`);
        } else {
            setStatus(`Error: ${data.detail}`);
        }
    } catch (err) {
        setStatus(`Upload failed: ${err.message}`);
    }
};

return (
    <Container sx={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
    <Typography level="body-md" sx={{margin: 8}}>
        Here you can upload the msesy csv files and it will 
        be parsed and return a clean CSV.
    </Typography>
    <Box sx={{ display: 'flex', flexDirection:'row', justifyContent: 'center'}}>
        <Card variant="outlined" sx={{ width: 400, p: 3, textAlign: "center"}}>
            <Typography level="h4" sx={{ mb:2 }}>
                Upload CSV File
            </Typography>

            <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                style={{ marginBottom: "1rem"}}
            />

            <Button onClick={handleUpload} variant="solid" fullWidth>
                Upload
            </Button>

            { status && (
                <Typography level="body-sm" sx={{ mt: 2}}>
                    {status}
                </Typography>
            )}
        </Card>
    </Box>
    </Container>
    )
}
