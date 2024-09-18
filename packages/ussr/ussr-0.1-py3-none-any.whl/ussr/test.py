from ussr.reencoder import UniversalSentenceSearchReencoder


def search(query, corpus):
    reencoder = UniversalSentenceSearchReencoder()

    query_embedding = reencoder.generate_embeddings(query)
    result_scores = []
    for sentence in corpus:
        embedding = reencoder.generate_embeddings(sentence)
        similarity = reencoder.cosine_similarity(query_embedding, embedding)
        result_scores.append((similarity, sentence))
    sorted_results = sorted(result_scores, key=lambda x: x[0], reverse=True)
    for score, sentence in sorted_results:
        if score > 0.5:
            print(f"Match: {sentence}")
            print("---")
            print(f"Similarity: {score}")


# Example corpus (each sentence in the novel becomes an entry)
corpus = [
    "Marie's Birthday Cake 🎂  Birthday Cute ",
    "Chocolate 24/7😵‍💫 Strawberry Chocolate Love Amazing ",
    "Rainbow goodness🌈 Mixed Fruit Yummy Rainbow Sweet ",
    "Fluffy lamb cake Strawberry Fluffy Lamb Pink ",
    "Birthday Cake Cherry Cream Cheese Blueberry Birthday Cake Sweet Cute Pink ",
    "Our First Ever Post 🥳 Chocolate Sweet Amazing Flavorful ",
    "Our store",
    "Fig Cake  Fig Cake Sweet ",
    "valentines treat  dont wait until its too late to get your valentines day cake come grab our gift box and have a cute picnic with your loved one valentines cake love strawberry chocolate ",
    "Chocolate cake Chocolate Cozy Sweet ",
    "Birthday cake Chocolate Vanilla Birthday cake Sweet Cute ",
    "Celebratory cake Cherry Celebration Macaron ",
    "Pancakes🤔 Strawberry Mixed Fruit Blueberry Pancakes ",
    "chocolate cinnamon cake  best dessert we have for sale  come grab yours at a reasonable price  cinnamon sweet dessert chocolate ",
    "Cupcakes 🤔 Chocolate Cupcakes Freshstart ",
    "Fig Cake 🎂  Vanilla Cream Cheese Fig Sweet ",
    "Chocolate and Cherry cake Chocolate Cherry Amazing ",
    "Cupcakes🤗🧁 Cherry Blueberry Cupcake Sweet ",
    "Sweet pink and blue cake Cherry Vanilla Mixed Fruit Cream Cheese Pink Sweet Blue ",
    "All about the pink 🥰 Cherry Cream Cheese Pink Cake yourCake ",
    "Stitch cake Vanilla Mixed Fruit Cream Cheese Blueberry Lilo&stitch Cute ",
    "valentines day cake valentines day is around the corner dont wait until the last minute order your own cake from us valentin tortadebrecen epertora strawberry ",
    "Best birthday cake Only from your favorite bakery in Debrecen🙃❤️ Strawberry Cake Birthday",
    "gorgeous rosette cake the most beautiful pink cake we have made so far pink rose",
    "Cute Pink cake Cherry Cream Cheese Pink Cute ",
    "Pink cake Strawberry Cherry Sprinkles Pink Sweet ",
    "Cherry blossom cake Cherry Vanilla Cream Cheese Crimson Red ",
    "Oreo cake🤤🎂 Chocolate Vanilla Oreo Cake ",
    "Strawberry chocolate cake Strawberry Chocolate Sweet Amazing ",
    "have this fantastic cake for your child to enjoy their first birthday strawberry cherry blueberry childrens birthday cute cake",
    "Beautiful pink cake Strawberry Vanilla Cream Cheese Birthday Sweet Cute Pink ",
    "breakfast sharing some breakfast ideas best pancakes ever breakfast pancakes berries  ",
]
query = "Blueberry"
search(query, corpus)
