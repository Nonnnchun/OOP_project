from fasthtml.common import *

COMMON_STYLES = Style("""
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    :root {
        --primary-color: #FCDE22;
        --secondary-color: #F4D9C1;
        --dark-bg: #1a1f2c;
        --text-light: #E1EBF8;
        --accent-color: #D3ECDC;
        --error-color: #ff6b6b;
        --success-color: #51cf66;
    }

    body {
        margin: 0;
        padding: 0;
        min-height: 100vh;
        background: linear-gradient(135deg, var(--dark-bg), #2d3748, var(--dark-bg));
        font-family: 'Poppins', sans-serif;
        color: var(--text-light);
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .form-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        max-width: 500px;
        margin: 2rem auto;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-label {
        display: block;
        color: var(--text-light);
        margin-bottom: 0.5rem;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .form-input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-light);
        transition: all 0.3s ease;
        font-size: 1rem;
        font-family: 'Poppins', sans-serif;
    }

    .form-input:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(252, 222, 34, 0.2);
        background: rgba(255, 255, 255, 0.1);
    }

    .btn {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Poppins', sans-serif;
    }

    .btn-primary {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: var(--dark-bg);
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(252, 222, 34, 0.3);
    }

    .btn-secondary {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text-light);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    .title {
        color: var(--primary-color);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .error-message {
        color: var(--error-color);
        background: rgba(255, 107, 107, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }

    .success-message {
        color: var(--success-color);
        background: rgba(81, 207, 102, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
""")