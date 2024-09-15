import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';

const SignUp = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const handleSignUp = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        const formData = new FormData(e.currentTarget);
        const response = await fetch("https://formflow.org/auth", {
            method: "POST",
            body: formData,
            credentials: "include",
        });
        setLoading(false);
        if (response.ok) {
            navigate('/check-email/sign-up');
        } else {
            console.log(response.text());
            alert("There was an error logging in.");
        }
    };

    if (loading) {
        return <div id="loading"></div>;
    }

    return (
        <>
            <h2>Sign up</h2>
            <p className="center">
                Sign up with the email address that you want to use for receiving form submissions.
            </p>
            <form className="little" onSubmit={handleSignUp}>
                <input type="email" name="email_address" placeholder="Email address" required/>
                <button className="center" type="submit">Sign Up</button>
            </form>
        </>
    );
};

export default SignUp;
