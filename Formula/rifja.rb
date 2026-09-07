class Rifja < Formula
  include Language::Python::Virtualenv

  desc "Offline, evidence-aware continuity for local agent sessions and Git"
  homepage "https://github.com/0merUfuk/rifja"
  url "https://github.com/0merUfuk/rifja/releases/download/v0.2.0/rifja-0.2.0-py3-none-any.whl", using: :nounzip
  version "0.2.0"
  sha256 "0314997447f0d4357bde9f5f195045b239e9b39c29de738ae2c4a5b68030ed95"
  license "MIT"

  depends_on "git"
  depends_on "python@3.14"

  def install
    # The checked release wheel has no runtime Python dependencies. Installing
    # it directly avoids an unpinned build-backend download during installation.
    ENV["PIP_NO_INDEX"] = "1"
    venv = virtualenv_create(libexec, "python3.14", system_site_packages: false)
    venv.pip_install_and_link(buildpath/"rifja-0.2.0-py3-none-any.whl", build_isolation: false)
  end

  test do
    ENV["RIFJA_HOME"] = (testpath/"state").to_s
    assert_equal version.to_s, shell_output("#{bin}/rifja --version").strip
    system bin/"rifja", "setup", "--timezone", "Europe/Istanbul"
    system bin/"rifja", "doctor"
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
