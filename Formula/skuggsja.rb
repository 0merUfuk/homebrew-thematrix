# frozen_string_literal: true

# Generated from the release checksums; do not edit download values manually.
# Skuggsja release version: 0.1.1
class Skuggsja < Formula
  desc "Local history retrospective for AI coding agents"
  homepage "https://github.com/0merUfuk/skuggsja"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/0merUfuk/skuggsja/releases/download/v0.1.1/skuggsja_0.1.1_darwin_arm64.tar.gz"
      sha256 "4560a2eb42af8fe04b01899f2833e3b5dda5a1fe74943af2537562b32e0755b7"
    end
    on_intel do
      url "https://github.com/0merUfuk/skuggsja/releases/download/v0.1.1/skuggsja_0.1.1_darwin_amd64.tar.gz"
      sha256 "3079113535c1f5e05e868ebf837a57c5dca703f08f178d90c627edb8735bf87a"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/0merUfuk/skuggsja/releases/download/v0.1.1/skuggsja_0.1.1_linux_arm64.tar.gz"
      sha256 "2fab4bc62a6f426c9bbebc185b012c9b8ef6a71fdaa266ea6a6f8c9c8f1e2b57"
    end
    on_intel do
      url "https://github.com/0merUfuk/skuggsja/releases/download/v0.1.1/skuggsja_0.1.1_linux_amd64.tar.gz"
      sha256 "79300a2b081c94c41d90b93f3437cf9420d9096cf0ab31e6833810bcfb436610"
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
