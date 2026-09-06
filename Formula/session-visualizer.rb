class SessionVisualizer < Formula
  include Language::Python::Virtualenv

  desc "Offline, evidence-aware continuity for local agent sessions and Git"
  homepage "https://github.com/0merUfuk/session-visualizer"
  url "https://github.com/0merUfuk/session-visualizer/releases/download/v0.1.0/session_visualizer-0.1.0-py3-none-any.whl", using: :nounzip
  version "0.1.0"
  sha256 "cbcebf40ba24275cea324d7d684db1275c5a7175d4299fbc2aa0da2852f76334"
  license "MIT"

  depends_on "git"
  depends_on "python@3.14"

  def install
    # The checked release wheel has no runtime Python dependencies. Installing
    # it directly avoids an unpinned build-backend download during installation.
    ENV["PIP_NO_INDEX"] = "1"
    venv = virtualenv_create(libexec, "python3.14", system_site_packages: false)
    venv.pip_install_and_link(buildpath/"session_visualizer-0.1.0-py3-none-any.whl", build_isolation: false)
  end

  test do
    ENV["SESSION_VISUALIZER_HOME"] = (testpath/"state").to_s
    assert_equal version.to_s, shell_output("#{bin}/session-visualizer --version").strip
    system bin/"session-visualizer", "setup", "--timezone", "Europe/Istanbul"
    system bin/"session-visualizer", "doctor"
    system libexec/"bin/python", "-c", <<~PYTHON
      import sqlite3
      from compression import zstd
      from zoneinfo import ZoneInfo
      db = sqlite3.connect(':memory:')
      db.execute('CREATE VIRTUAL TABLE corpus USING fts5(text)')
      assert zstd.decompress(zstd.compress(b'roundtrip')) == b'roundtrip'
      assert ZoneInfo('Europe/Istanbul') is not None
    PYTHON
  end
end
