FROM rust:latest
WORKDIR /usr/src/app
COPY . .
RUN cargo build --release
EXPOSE 3001
CMD ["./target/release/rust-chat-backend"]