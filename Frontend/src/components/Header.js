import React from 'react';

const Header = ({ user, setUser }) => {
    const handleLogout = () => {
        setUser(null);
    };

    return (
        <header>
            <h1>Doctor Appointments</h1>
            {user ? (
                <div>
                    <span>Hola, {user.username}</span>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            ) : (
                <div>
                    <button onClick={() => setUser('login')}>Login</button>
                    <button onClick={() => setUser('signup')}>Sign Up</button>
                </div>
            )}
        </header>
    );
};

export default Header;
