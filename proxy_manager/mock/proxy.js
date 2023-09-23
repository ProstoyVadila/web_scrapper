const random = () => {
  return Math.floor(Math.random() * 255) + 1;
};

const randomIP = () => {
  return `${random()}.${random()}.${random()}.${random()}`;
};

const generateRandomProxy = () => {
  const ip = randomIP();
  const port = Math.floor(Math.random() * 65535) + 1;
  return {
    ip: ip,
    port: port,
  };
};

const server = Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response(JSON.stringify(generateRandomProxy()), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  },
});

console.log("Listening on http://localhost:3000");
