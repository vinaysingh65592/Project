import { PLATFORMS } from '../data/platforms';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-top">
          <div className="footer-brand">
            <div className="footer-logo">🚀 Deploy<span className="accent">Hub</span></div>
            <p>Your one-stop directory for free hosting platforms — covering every language, every framework.</p>
            <div className="footer-stats">
              <span>📦 {PLATFORMS.length}+ Platforms</span>
              <span>📖 10+ Guides</span>
              <span>🗄️ 8 Databases</span>
            </div>
          </div>
          <div className="footer-nav">
            <h4>Navigate</h4>
            <a href="#platforms">Explore Platforms</a>
            <a href="#compare">Top Picks</a>
            <a href="#guides">Deploy Guides</a>
            <a href="#databases">Free Databases</a>
          </div>
          <div className="footer-nav">
            <h4>Popular Platforms</h4>
            <a href="https://render.com" target="_blank" rel="noreferrer">Render</a>
            <a href="https://vercel.com" target="_blank" rel="noreferrer">Vercel</a>
            <a href="https://netlify.com" target="_blank" rel="noreferrer">Netlify</a>
            <a href="https://huggingface.co/spaces" target="_blank" rel="noreferrer">HuggingFace</a>
            <a href="https://railway.app" target="_blank" rel="noreferrer">Railway</a>
          </div>
        </div>
        <div className="footer-bottom">
          <p>Made with ❤️ for developers everywhere &bull; All platform data is community-sourced</p>
        </div>
      </div>
    </footer>
  );
}
