# Found this pretty nice Dockerfile on github (todo add a link). The size is extremly slow and the file doesn't look too sophisticated.
# TODO: don't forget to add additinal dependencies for your project.

FROM rust:1.72.0-alpine3.17 as builder
# This is important, see https://github.com/rust-lang/docker-rust/issues/85
ENV RUSTFLAGS="-C target-feature=-crt-static"
# if needed, add additional dependencies here
RUN apk add --no-cache musl-dev pkgconfig openssl-dev
# set the workdir and copy the source into it
WORKDIR /app
COPY ./extractor /app
# do a release build
RUN cargo build --release
RUN strip target/release/extractor

# use a plain alpine image, the alpine version needs to match the builder
FROM alpine:3.17
# if needed, install additional dependencies here
RUN apk add --no-cache libgcc
# copy the binary into the final image
COPY --from=builder /app/target/release/extractor .
# set the binary as entrypoint
ENTRYPOINT ["/extractor"]
