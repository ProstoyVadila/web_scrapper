use crate::config;

use sqlx::postgres::PgPoolOptions;

const MAX_POOL_SIZE: u32 = 10;

pub struct Database {
    #[allow(dead_code)]
    pool: sqlx::PgPool,
}

impl Database {
    pub async fn new(conf: config::ConfigPostgres) -> Result<Database, sqlx::Error> {
        let pool = PgPoolOptions::new()
            .max_connections(MAX_POOL_SIZE)
            .connect(&conf.get_url())
            .await?;
        Ok(Database { pool })
    }

    // pub async fn get(&self, id: i32) -> Result<models::User, sqlx::Error> {
    //     let user = sqlx::query_as::<_, models::User>("SELECT * FROM users WHERE id = $1")
    //         .bind(id)
    //         .fetch_one(&self.pool)
    //         .await?;
    //     Ok(user)
    // }
}
