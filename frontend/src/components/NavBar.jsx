import { Sheet, Typography, Button, Stack } from "@mui/joy";
import { Link } from "react-router-dom";

const NavBar = () => {
    return (
        <Sheet
            variant="solid"
            color="primary"
            sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                p: 2,
            }}>
            <Typography level="h4" component="h1" sx={{ color: "white"}}>
                MyApp
            </Typography>
            <Stack direction="row" spacing={2}>
                <Button component={Link} to="/" variant="soft" color="neutral">
                    Home
                </Button>
                <Button component={Link} to="/mapping" variant="soft" color="neutral">
                    Mapping
                </Button>
                <Button component={Link} to="/load" variant="soft" color="neutral">
                    Load
                </Button>
                <Button component={Link} to="/validation" variant="soft" color="neutral">
                    Validation
                </Button>
                <Button component={Link} to="/chat" variant="soft" color="neutral">
                    Chat
                </Button>
            </Stack>
        </Sheet>
    )
}

export default NavBar;