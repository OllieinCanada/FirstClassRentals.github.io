.nav-toggle:checked + ul {
    display: flex;
  }
  
  .nav-toggle-label {
    display: none;
    position: absolute;
    right: 20px;
    top: 20px;
  }
  
  @media (max-width: 768px) {
    .nav-toggle-label { display: block; }
    .navbar ul { flex-direction: column; }
  }
  