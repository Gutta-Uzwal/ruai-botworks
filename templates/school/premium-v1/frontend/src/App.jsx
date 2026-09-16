const navigation = [
  ["About", "/about"],
  ["Admissions", "/admissions"],
  ["Academics", "/academics"],
  ["Campus life", "/campus-life"],
  ["Contact", "/contact"],
];

export default function App() {
  return (
    <div className="site-shell">
      <header className="site-header">
        <a className="brand" href="/">
          School
        </a>
        <nav aria-label="Primary navigation">
          {navigation.map(([label, href]) => (
            <a href={href} key={href}>
              {label}
            </a>
          ))}
        </nav>
      </header>
      <main>
        <section className="hero" aria-labelledby="hero-title">
          <p className="eyebrow">Learning with purpose</p>
          <h1 id="hero-title">A welcoming place to grow, learn, and belong.</h1>
          <p>
            Discover a thoughtful education shaped around curiosity, confidence,
            and community.
          </p>
          <a className="button" href="/admissions">
            Explore admissions
          </a>
        </section>
      </main>
      <footer>School · Public information site</footer>
    </div>
  );
}
