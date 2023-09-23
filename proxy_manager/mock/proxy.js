const proxy = {
  name: "proxy",
  addr: "afsdf",
  password: "123456",
};

const server = Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response(JSON.stringify(proxy), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  },
});

console.log("Listening on http://localhost:3000");
