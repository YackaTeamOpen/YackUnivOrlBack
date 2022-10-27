-- Préférences
INSERT INTO `music_pref` (`id`, `label`) VALUES
(1, 'Non'),
(2, 'Oui');

INSERT INTO `speaking_pref` (`id`, `label`) VALUES
(1, 'Non'),
(2, 'Oui');

INSERT INTO `smoking_pref` (`id`, `label`) VALUES
(1, 'Non'),
(2, 'Oui');

-- Bills
INSERT INTO `bill` (`id`, `price`, `nb_max_employees`) VALUES (NULL, '2500', '10000');

-- Entreprise pour compte administrateur
INSERT INTO `organization` (`id`, `name`, `siret`, `address`, `creation_date`, `bill_id`) VALUES
(1, 'Yacka', '85049412100013', '3 Ruelle de la prez 41500 Saint-Dye-Sur-Loire', '2016-12-21 00:00:00.000', NULL),
(2, 'test_company', '123456789012345', '27 route des Primevères 45000 Orléans', '2016-12-21 00:00:00.000', 1);

-- Compte yacka et admin test company
INSERT INTO `user`
(`type`, `password_hash`, `name`, `surname`, `email`, `phone`, `public_phone`, `gender`,`organization_id`,`speaking_pref_id`, `smoking_pref_id`, `music_pref_id`,`creation_date`,`email_ok`,`cgu`,`last_login`) VALUES
(0, '','Yacka', 'Yacka', 'admin_yacka', '', TRUE, 'H', 1,1,1,1,'2016-12-21 00:00:00.000', TRUE, 1, '2016-12-21 00:00:00.000'),
(1, '$2b$12$19jLO58R9HJlUXebZotcdOVjhjRtEU/Ec7cKrdAQc6TAa7wAb3JJK','test_company', 'test_company', 'testco@yacka.fr', '', TRUE, 'F', 2,1,1,1,'2016-12-21 00:00:00.000', TRUE, 1, '2016-12-21 00:00:00.000');

-- Problèmes signalables
INSERT INTO `problem` (`id`, `comment`) VALUES
(1, 'Comportement inapproprié'),
(2, 'Retard'),
(3, 'Absent'),
(4, 'Contenu inapproprié'),
(5, 'Information erronée'),
(6, 'Autre');

-- Message d'accueil
INSERT INTO `welcome_msg` (`id`, `message`, `state`) VALUES (NULL, 'Merci d\'utiliser Yacka', '1');

