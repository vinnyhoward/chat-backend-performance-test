use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use mongodb::{Client, options::ClientOptions};
use serde::{Deserialize, Serialize};
use bson::{doc, Document};

#[derive(Debug, Serialize, Deserialize)]
struct Message {
    content: String,
}

async fn create_message(msg: web::Json<Message>, data: web::Data<Client>) -> impl Responder {
    let collection = data.database("chatdb").collection::<Document>("messages");
    let doc = doc! { "content": msg.content.clone() };
    match collection.insert_one(doc).await {
        Ok(result) => HttpResponse::Ok().json(result.inserted_id),
        Err(e) => HttpResponse::InternalServerError().body(e.to_string()),
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let client_options = ClientOptions::parse("mongodb://mongodb:27017").await.unwrap();
    let client = Client::with_options(client_options).unwrap();

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(client.clone()))
            .service(web::resource("/message").route(web::post().to(create_message)))
    })
    .bind("0.0.0.0:3001")?
    .run()
    .await
}

