/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      { source: "/comparison", destination: "/lab", permanent: false },
      { source: "/history", destination: "/lab", permanent: false },
      { source: "/history/:path*", destination: "/lab", permanent: false },
    ];
  },
};

module.exports = nextConfig;
