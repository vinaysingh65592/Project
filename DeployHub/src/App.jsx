import { useState, useEffect, useRef } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import PlatformsSection from './components/PlatformsSection';
import CompareSection from './components/CompareSection';
import GuidesSection from './components/GuidesSection';
import DatabasesSection from './components/DatabasesSection';
import Footer from './components/Footer';
import './App.css';

export default function App() {
  const [search, setSearch] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Keyboard shortcut "/" to focus search
  useEffect(() => {
    const handler = (e) => {
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        document.getElementById('searchInput')?.focus();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  return (
    <div className="app">
      <Navbar theme={theme} setTheme={setTheme} />
      <Hero search={search} setSearch={setSearch} />
      <PlatformsSection search={search} activeFilter={activeFilter} setActiveFilter={setActiveFilter} />
      <CompareSection />
      <GuidesSection />
      <DatabasesSection />
      <Footer />
    </div>
  );
}
