/**
 * Research Publications Data Structure
 *
 * This file contains all research publication information displayed on the Research page.
 * All fields are optional - if a field is missing or empty, it will be gracefully handled
 * using the builder pattern in the ResearchCard component.
 *
 * To edit:
 * 1. Update the values in the researchData object below
 * 2. You can remove any field from a research entry if you don't want to display it
 * 3. Set is_visible to false to hide an entry without deleting it
 * 4. Use display_order to control the order of research items (lower numbers appear first)
 */

export interface ResearchPublication {
  id?: string;                          // Unique identifier
  title?: string;                       // Research paper title
  authors?: string[];                   // Array of author names
  publication_date?: string;            // Publication date (e.g., "2023", "2024-09-11")
  institution?: string;                 // Institution (for thesis/dissertations)
  book?: string;                        // Book/Conference name
  publisher?: string;                   // Publisher name
  pages?: string;                       // Page numbers (e.g., "229-250")
  publication_type?: string;            // e.g., "Conference Paper", "Journal Article", "Thesis"
  description?: string;                 // Brief description/abstract
  abstract?: string;                    // Full abstract (alternative to description)
  objectives?: string[];                // Research objectives
  methods_used?: string[];              // Methods/approaches used
  models_tested?: string[];             // ML models tested
  dataset?: string;                     // Dataset name
  dataset_source?: string;              // Dataset source URL
  metrics?: string[];                   // Evaluation metrics
  evaluation_metrics?: string[];        // Alternative to metrics
  comparison_models?: string[];         // Models compared against
  results_summary?: string;             // Summary of results
  highlights?: string[];                // Key highlights
  tags?: string[];                      // Tags for categorization
  url?: string;                         // Publication URL (DOI, Google Scholar, etc.)
  pdf_url?: string;                     // Direct PDF link
  github_url?: string;                  // GitHub repository
  doi?: string;                         // Digital Object Identifier
  citations?: number;                   // Citation count
  is_visible?: boolean;                 // Set to false to hide this entry (default: true)
  display_order?: number;               // Order of display (lower numbers appear first)
}

export interface ResearchData {
  research_publications: ResearchPublication[];
}

export const researchData: ResearchData = {
  "research_publications": [
    {
      "id": "skin_cancer_cnn_research",
      "title": "Application of Deep Convolutional Neural Network in Multiclass Skin Cancer Classification Using Custom CNN Architecture",
      "authors": [
        "Nadia Shafique",
        "Kaynat Bint Shaheen",
        "Zarjis Husain Sikder",
        "Utsho Dey",
        "Sharforaz Rahman Swacha"
      ],
      "publication_date": "2023",
      "institution": "Brac University",
      "publication_type": "Undergraduate Thesis / Research Paper",
      "description": "This research proposes a custom CNN architecture for the classification of multiple skin diseases using 28x28 RGB images from the HAM10000 dataset. The model demonstrates superior performance in accuracy and efficiency compared to established pre-trained networks like ResNet50 and EfficientNetB0/B2.",
      "objectives": [
        "Develop a custom CNN model for multiclass skin disease classification.",
        "Compare performance with pre-trained models (ResNet50, EfficientNetB0/B2).",
        "Reduce training time and parameter complexity for efficient deployment."
      ],
      "dataset": "HAM10000",
      "metrics": ["Accuracy", "Precision", "Recall", "F1-Score"],
      "comparison_models": ["ResNet50", "EfficientNetB0", "EfficientNetB2"],
      "results_summary": "The proposed model achieved higher test accuracy with fewer trainable parameters and faster training per epoch than existing pre-trained models, making it suitable for resource-constrained environments.",
      "highlights": [
        "Improved test accuracy and reduced test loss.",
        "Lightweight model with lower computational requirements.",
        "Demonstrates potential for clinical diagnostic deployment."
      ],
      "tags": [
        "Deep Learning",
        "CNN",
        "Medical Imaging",
        "Healthcare AI",
        "Computer Vision"
      ],
      "url": "https://scholar.google.com/scholar?cluster=1234567890",
      "is_visible": true,
      "display_order": 1
    },
    {
      "id": "house_price_prediction",
      "title": "Tailored House Price Prediction Insights for Dhaka and Chittagong City",
      "authors": [
        "Utsho Dey",
        "Md Sakhawat Hossain Rabbi",
        "Md Abrar Hamim",
        "Md Tarek Habib"
      ],
      "publication_date": "2024-09-11",
      "book": "International Conference on Electrical and Electronics Engineering (ICEEE)",
      "publisher": "Springer Nature Singapore",
      "pages": "229-250",
      "publication_type": "Conference Paper",
      "dataset_source": "https://bdproperty.com/",
      "description": "This paper explores the use of advanced machine learning models to predict housing prices in Dhaka and Chittagong. Using a 3-year dataset, the study applies models such as XGBoost, Random Forest, and Linear Regression to evaluate performance based on R-squared and MSE metrics.",
      "objectives": [
        "Build accurate predictive models for house pricing in Bangladesh.",
        "Analyze the impact of data preprocessing and feature scaling on model accuracy.",
        "Compare traditional and ensemble ML methods for prediction."
      ],
      "methods_used": [
        "Data Preprocessing",
        "Feature Engineering",
        "Model Comparison",
        "Evaluation Metrics Analysis"
      ],
      "models_tested": ["Linear Regression", "Random Forest", "XGBoost"],
      "evaluation_metrics": ["R²", "Mean Squared Error (MSE)"],
      "results_summary": "Random Forest achieved the highest prediction accuracy, emphasizing the significance of preprocessing and feature selection for regression tasks.",
      "highlights": [
        "Comprehensive study on Dhaka and Chittagong housing markets.",
        "Feature scaling significantly improved performance metrics.",
        "Published in Springer Nature's conference proceedings."
      ],
      "tags": [
        "Machine Learning",
        "Regression",
        "Real Estate Analytics",
        "Data Science",
        "XGBoost"
      ],
      "url": "https://link.springer.com/chapter/10.xxxxxxx",
      "is_visible": true,
      "display_order": 2
    }
  ]
};

/**
 * Example: Adding a new research publication with minimal fields
 * (All fields are optional - remove any you don't need)
 *
 * {
 *   "id": "my_research",
 *   "title": "My Research Title",
 *   "authors": ["Author 1", "Author 2"],
 *   "publication_date": "2025",
 *   "publication_type": "Journal Article",
 *   "description": "Brief description of the research",
 *   "tags": ["AI", "Machine Learning"],
 *   "is_visible": true,
 *   "display_order": 1
 * }
 *
 * The builder pattern in ResearchCard.astro will handle any missing fields gracefully.
 */
