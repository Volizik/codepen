const { Sequelize, DataTypes, Model } = require('sequelize');

const sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USER, process.env.DB_PASSWORD, {
    host: process.env.DB_HOST,
    dialect: 'mysql',
});

const init = async (callback) => {
    await sequelize.sync();
    callback?.();
}

class Pen extends Model {}
Pen.init({
    link: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
    },
    name: DataTypes.STRING,
    likes: DataTypes.STRING,
    author: DataTypes.STRING,
    image: DataTypes.STRING,
    posted: {
        type: DataTypes.BOOLEAN,
        defaultValue: false,
    },
}, { sequelize, modelName: 'Pen' });

module.exports = {
    Pen,
    init,
}

