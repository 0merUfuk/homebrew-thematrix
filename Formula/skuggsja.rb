# frozen_string_literal: true

# Generated from the release checksums; do not edit download values manually.
# Skuggsja release version: 0.1.0
class Skuggsja < Formula
  desc "Local history retrospective for AI coding agents"
  homepage "https://github.com/0merUfuk/skuggsja"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/0merUfuk/skuggsja/releases/download/v0.1.0/skuggsja_0.1.0_darwin_arm64.tar.gz"
      sha256 "6fcf0b6805990deacd0e0b9990d054966c562d1c002cf5176848d45c6c3aa152"
    end
    on_intel do
      url "https://github.com/0merUfuk/skuggsja/releases/download/v0.1.0/skuggsja_0.1.0_darwin_amd64.tar.gz"
      sha256 "b1391212f37a3afd40373f2cd3aaab13025e145a9da24a56a3f333c59169dfcc"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/0merUfuk/skuggsja/releases/download/v0.1.0/skuggsja_0.1.0_linux_arm64.tar.gz"
      sha256 "388c7553e1894d544c5edaddc86b585cd34a6e6a7c36898de5a04388da8fc5e8"
    end
    on_intel do
      url "https://github.com/0merUfuk/skuggsja/releases/download/v0.1.0/skuggsja_0.1.0_linux_amd64.tar.gz"
      sha256 "3528bfce2ef2f717bd887d1d419c2941761f18683c308bd4099dd5cd63ecb808"
    end
  end

  def install
    bin.install "skuggsja"
    generate_completions_from_executable(bin/"skuggsja", "completion")
  end

  test do
    assert_equal "skuggsja #{version}", shell_output("#{bin}/skuggsja version").strip
    assert_match "--no-open", shell_output("#{bin}/skuggsja --help")
  end
end
