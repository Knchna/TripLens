/**
 * TripLens AI - Data Model & Mock Store
 * Rich structured dataset for Himachal (HP002 - HP015) & Kerala (KE001) packages,
 * agency metadata, source URLs, customer reviews, and AI decision metrics.
 */

const TRIPWISE_DATA = {
  defaultRequest: "I want a 6-day Shimla & Manali trip from Delhi for 2 people between ₹12,000 and ₹22,000, focused on snow points, scenic views, and relaxed pacing.",

  suggestionChips: [
    { label: "🏔️ Shimla & Manali (6 Days)", query: "I want a 6-day Shimla and Manali trip from Delhi for 2 people between ₹12,000 and ₹20,000 with Solang Valley and relaxed pace.", destination: "Himachal (Shimla/Manali)", minBudget: 12000, maxBudget: 20000, duration: 6 },
    { label: "🏔️ Grand Himachal (9 Days)", query: "I want a 9-day full Himachal circuit from Delhi covering Shimla, Manali, Dalhousie and Amritsar between ₹22,000 and ₹30,000.", destination: "Himachal (Shimla/Manali)", minBudget: 22000, maxBudget: 30000, duration: 9 },
    { label: "🏡 Jibhi & Offbeat (7 Days)", query: "I want a 7-day offbeat trip from Delhi to Shimla, Manali and Jibhi valley between ₹18,000 and ₹25,000.", destination: "Himachal (Shimla/Manali)", minBudget: 18000, maxBudget: 25000, duration: 7 },
    { label: "🌿 Kerala Backwaters & Tea", query: "I want a 5-day Kerala trip from Bangalore for 2 people between ₹20,000 and ₹30,000 focused on tea gardens and backwaters.", destination: "Kerala", minBudget: 20000, maxBudget: 30000, duration: 5 },
    { label: "💰 Express Budget (4 Days)", query: "I want a quick 4-day weekend trip to Shimla and Manali under ₹15,000 from Delhi.", destination: "Himachal (Shimla/Manali)", minBudget: 10000, maxBudget: 15000, duration: 4 }
  ],

  defaultPreferences: {
    minBudget: 12000,
    maxBudget: 22000,
    duration: 6,
    from: "Delhi",
    travelers: 2,
    destination: "Himachal (Shimla/Manali)",
    pace: "Relaxed"
  },

  packages: [
    {
      id: "hp002",
      packageCode: "HP002",
      title: "Shimla, Manali & Kasol Valley Escapade",
      subtitle: "Misty Valleys, Manikaran Sahib & Riverside Camping",
      agency: "KingHills Travels",
      agencyType: "Independent Niche Agency",
      agencyRating: 4.8,
      sourceUrl: "https://kinghillstravels.com/packages/hp002-shimla-manali-kasol",
      price: 13800,
      originalPrice: 16500,
      duration: "6 Days / 5 Nights",
      durationDays: 6,
      durationNights: 5,
      destination: "Himachal (Shimla/Manali)",
      origin: "Delhi",
      hotel: "3★ Valley View Hotel & Kasol Riverside Camp",
      hotelName: "Snow Valley Heights & Kasol Pines Camp",
      hotelRating: 4.8,
      image: "assets/hero-himachal.jpg",
      fitScore: 96,
      valueScore: 94,
      itineraryScore: 92,
      trustScore: 91,
      rating: 4.8,
      totalReviews: 142,
      badge: "AI TOP RECOMMENDATION",
      badgeIcon: "🤖",
      badgeExplanation: "Perfect match for budget ₹12k–₹22k with Solang Valley, Manikaran Sahib, and included Bonfire party.",
      summary: "Explore Mall Road Shimla, Jakhoo Temple, Solang Valley, Atal Tunnel, and Kasol's serene Manikaran Sahib with night travel optimization.",

      overview: {
        durationText: "6 Days / 5 Nights",
        travelersText: "2 Travelers",
        startingCity: "Starting from Delhi (9 AM Volvo/Cab)",
        focusText: "Snow Points & Rivers",
        paceText: "Balanced & Scenic"
      },

      whyMatches: {
        fitPercent: 96,
        reasons: [
          { text: "Within your budget range (₹13,800 vs ₹12,000–₹22,000)", positive: true },
          { text: "Includes Solang Valley, Atal Tunnel & Sissu Village access", positive: true },
          { text: "Includes Kasol & Manikaran Sahib hot springs with Langar meal", positive: true },
          { text: "Complimentary Bonfire & Music Party in Manali included", positive: true },
          { text: "Note: Rohtang Pass permit carries optional extra charges if visited", positive: false }
        ]
      },

      costBreakdown: {
        packagePrice: 13800,
        estimatedAdditional: 1200,
        effectiveTotal: 15000,
        explanation: "Effective Total includes package price plus estimated out-of-pocket activities and permits.",
        items: [
          { label: "Advertised Package Price (KingHills Travels)", amount: 13800, type: "base" },
          { label: "Kufri pony rides / optional snow boots", amount: 500, type: "additional" },
          { label: "Kullu rafting & paragliding (optional activity)", amount: 500, type: "additional" },
          { label: "Driver bata & highway state tolls", amount: 200, type: "additional" }
        ]
      },

      inclusions: [
        "Deluxe stay in Shimla & Manali with 1 night Kasol river camp",
        "Daily Breakfast & Dinner at all hotels (5 Breakfasts, 4 Dinners)",
        "Delhi to Shimla & Manali to Delhi Volvo/Cab transfers",
        "Sightseeing in Kufri, Solang Valley, Atal Tunnel & Manikaran",
        "Complimentary Bonfire & DJ Music Night in Manali",
        "All driver allowances, parking, and toll taxes"
      ],

      exclusions: [
        "Rohtang Pass NGT permit & local taxi charges (~₹1,500/cab)",
        "Kullu river rafting and paragliding ticket fees",
        "Personal expenses, laundry, heater charges",
        "Lunches during travel days (except complimentary Langar at Manikaran)"
      ],

      itinerary: [
        {
          day: 1,
          route: "Delhi → Shimla",
          tagline: "Drive to the Queen of Hills",
          intensity: "Moderate",
          intensityLevel: "moderate",
          transitHours: "8 hrs",
          distanceKm: "340 km",
          meals: "Lunch & Dinner",
          activities: [
            "Departure from Delhi around 9:00 AM via scenic NH44",
            "En-route lunch break at Himalayan Expressway enclave",
            "Evening arrival in Shimla, hotel check-in & leisure stroll on Mall Road"
          ],
          warnings: []
        },
        {
          day: 2,
          route: "Shimla Sightseeing & Night Transit",
          tagline: "Colonial Charm & Kufri Meadows",
          intensity: "High",
          intensityLevel: "high",
          transitHours: "Drive + Night Transit",
          distanceKm: "260 km",
          meals: "Breakfast",
          activities: [
            "Visit Green Valley, Fagu Valley & Kufri snow viewpoint",
            "Explore St. Christ Church, The Ridge, Scandal Point & Jakhoo Temple",
            "10:00 PM overnight transit journey to Manali"
          ],
          warnings: ["⚠️ Night drive from Shimla to Manali departs at 10 PM"]
        },
        {
          day: 3,
          route: "Manali Local Sightseeing",
          tagline: "Valley of the Gods",
          intensity: "Low",
          intensityLevel: "low",
          transitHours: "Local",
          distanceKm: "40 km",
          meals: "Breakfast & Dinner",
          activities: [
            "Early morning check-in (~3 AM) and rest till 10 AM",
            "Visit Vashisht Hot Springs & Temple, Jogini Waterfall trek",
            "Explore Hadimba Temple, Van Vihar, Tibetan Monastery & Mall Road"
          ],
          warnings: []
        },
        {
          day: 4,
          route: "Manali → Solang Valley & Atal Tunnel",
          tagline: "Snow Peaks & High Altitude Tunnels",
          intensity: "Moderate",
          intensityLevel: "moderate",
          transitHours: "3 hrs",
          distanceKm: "60 km",
          meals: "Breakfast & Dinner",
          activities: [
            "Excursion to Solang Valley snow adventure zone",
            "Drive through engineering marvel Atal Tunnel to Sissu Village (if open)",
            "Optional Rohtang Pass trip (subject to permit & extra cost)",
            "Evening Bonfire & Music Party at hotel included"
          ],
          warnings: ["⚠️ Rohtang Pass entrance requires separate NGT permit fees"]
        },
        {
          day: 5,
          route: "Manali → Kasol & Manikaran Sahib → Delhi",
          tagline: "Parvati Valley & Sacred Springs",
          intensity: "High",
          intensityLevel: "high",
          transitHours: "Overnight drive",
          distanceKm: "520 km",
          meals: "Breakfast (Langar dinner complimentary)",
          activities: [
            "Stop at Kullu Rafting & Paragliding point",
            "Explore Kasol flea market & Manikaran Sahib Gurudwara hot springs",
            "Enjoy complimentary Langar dinner at Manikaran Gurudwara",
            "Night departure proceeding to Delhi"
          ],
          warnings: ["⚠️ Kullu rafting activity fees are payable directly on spot"]
        },
        {
          day: 6,
          route: "Delhi Arrival",
          tagline: "Homeward Bound",
          intensity: "Low",
          intensityLevel: "low",
          transitHours: "Morning arrival",
          distanceKm: "0 km",
          meals: "None",
          activities: [
            "Early morning arrival in Delhi (~7 AM)",
            "Trip concludes with lifelong Himalayan memories"
          ],
          warnings: []
        }
      ],

      trustInsights: {
        score: 91,
        totalReviews: 142,
        sentiment: { positive: 89, neutral: 8, negative: 3 },
        aspects: [
          {
            name: "Hotel & Stay",
            icon: "🏨",
            score: "4.8 / 5",
            sentimentType: "positive",
            positives: [
              "Clean, cozy mountain rooms with hot water 24x7",
              "Kasol riverside camp was memorable with bonfire"
            ],
            concern: "Early check-in at 3 AM on Day 3 can feel chilly"
          },
          {
            name: "Transport & Cab",
            icon: "🚗",
            score: "4.7 / 5",
            sentimentType: "positive",
            positives: [
              "Experienced Himalayan mountain driver",
              "Comfortable sedan cab with heated blowers"
            ],
            concern: "Night drive from Shimla to Manali requires heavy warm clothing"
          },
          {
            name: "Itinerary & Value",
            icon: "🗺️",
            score: "4.9 / 5",
            sentimentType: "positive",
            positives: [
              "Covers maximum sights (Shimla, Manali, Kasol, Manikaran)",
              "Includes Atal Tunnel and free bonfire party"
            ],
            concern: "Rohtang pass taxi cost is extra"
          },
          {
            name: "Agency Support",
            icon: "💬",
            score: "4.8 / 5",
            sentimentType: "positive",
            positives: [
              "KingHills coordinator called daily to verify cab arrival",
              "Fast resolution when Sissu tunnel road was temporarily paused"
            ],
            concern: "None reported"
          }
        ],
        reviewsList: [
          { name: "Rahul S.", rating: 5.0, date: "Aug 2026", comment: "KingHills Travels organized everything flawlessly! Solang Valley and Manikaran Sahib hot springs were the highlights." },
          { name: "Priya & Amit", rating: 4.8, date: "Jul 2026", comment: "Super value package under ₹15,000. Driver Sunita was very polite and knew the best photo spots in Shimla." },
          { name: "Vikram M.", rating: 4.7, date: "Jun 2026", comment: "Great itinerary! The bonfire night in Manali was super fun. Highly recommend KingHills for Himachal trips." }
        ]
      }
    },

    {
      id: "hp003",
      packageCode: "HP003",
      title: "Grand Himachal Circuit with Dalhousie & Amritsar",
      subtitle: "Shimla, Manali, Kangra Valley, Khajjiar & Golden Temple",
      agency: "Thrillophilia",
      agencyType: "Verified Niche Marketplace Partner",
      agencyRating: 4.7,
      sourceUrl: "https://www.thrillophilia.com/tours/hp003-grand-himachal-circuit",
      price: 28500,
      originalPrice: 32000,
      duration: "9 Days / 8 Nights",
      durationDays: 9,
      durationNights: 8,
      destination: "Himachal (Shimla/Manali)",
      origin: "Delhi",
      hotel: "3★ Deluxe Mountain Resorts & Heritage Hotel",
      hotelName: "Shimla Ridge & Dalhousie Pines Resort",
      hotelRating: 4.7,
      image: "assets/hero-himachal.jpg",
      fitScore: 92,
      valueScore: 90,
      itineraryScore: 94,
      trustScore: 90,
      rating: 4.7,
      totalReviews: 198,
      badge: "HUMAN AI PICK • FULL CIRCUIT",
      badgeIcon: "🧠",
      badgeExplanation: "Recommended by AI: Slightly above ₹22k max budget, but adds 3 extra days covering Kangra, Dalhousie, Khajjiar & Amritsar Golden Temple.",
      summary: "The ultimate 9-day Himalayan panorama taking you from Shimla and Manali across Kangra Valley to Dalhousie, Khajjiar (Mini Switzerland) and Wagah Border.",

      overview: {
        durationText: "9 Days / 8 Nights",
        travelersText: "2 Travelers",
        startingCity: "Starting from Delhi",
        focusText: "Full Circuit & Culture",
        paceText: "Comprehensive & Active"
      },

      whyMatches: {
        fitPercent: 92,
        reasons: [
          { text: "AI Recommendation: ₹6,500 above max budget, but includes 3 additional destinations (Kangra, Dalhousie, Amritsar)", positive: true },
          { text: "Covers Khajjiar ('Mini Switzerland of India') & HPCA Stadium Dharamshala", positive: true },
          { text: "Includes Wagah Border ceremony & Golden Temple evening illumination", positive: true },
          { text: "Daily Breakfast & Dinner included across all 8 nights", positive: true },
          { text: "Longer 9-day duration ideal for deep mountain exploration", positive: true }
        ]
      },

      costBreakdown: {
        packagePrice: 28500,
        estimatedAdditional: 1800,
        effectiveTotal: 30300,
        explanation: "Effective Total estimates out-of-pocket costs like optional paragliding and monument tickets.",
        items: [
          { label: "Advertised Package Base Price (Thrillophilia)", amount: 28500, type: "base" },
          { label: "Paragliding & Rafting self-pay ticket allowance", amount: 1000, type: "additional" },
          { label: "Khajjiar & HPCA stadium entrance tickets", amount: 450, type: "additional" },
          { label: "Driver bata & interstate vehicle taxes", amount: 350, type: "additional" }
        ]
      },

      inclusions: [
        "8 nights accommodation in handpicked 3★ scenic hotels",
        "Daily Breakfast & Dinner (8 Breakfasts, 7 Dinners)",
        "Private AC Sedan/SUV for full 9-day Delhi-to-Delhi circuit",
        "Sightseeing in Shimla, Manali, Kangra, Dalhousie, Khajjiar & Amritsar",
        "Wagah Border & Golden Temple visit",
        "All toll taxes, parking, driver night allowances"
      ],

      exclusions: [
        "Rohtang Pass NGT permit taxi cost",
        "Paragliding, River Rafting & Cable car fees at Solang/Kangra",
        "Personal expenses, telephone, laundry",
        "Lunch meals on transit routes"
      ],

      itinerary: [
        { day: 1, route: "Delhi to Shimla", tagline: "Scenic Drive to Shimla", intensity: "Moderate", transitHours: "8 hrs", distanceKm: "340 km", meals: "Lunch & Dinner", activities: ["9 AM departure from Delhi", "Scenic hill ascent via Solan", "Hotel check-in & Mall Road leisure"], warnings: [] },
        { day: 2, route: "Shimla Sightseeing", tagline: "Green Valley & Kufri", intensity: "High", transitHours: "Drive + Night transit", distanceKm: "260 km", meals: "Breakfast & Dinner", activities: ["Kufri, Green Valley & Fagu Valley", "Ridge, Christ Church & Jakhoo Temple", "10 PM night departure to Manali"], warnings: [] },
        { day: 3, route: "Manali Local", tagline: "Temples & Monasteries", intensity: "Low", transitHours: "Local", distanceKm: "30 km", meals: "Breakfast & Dinner", activities: ["Early morning arrival (~3 AM check-in)", "Vashisht Hot Spring & Jogini Falls trek", "Hadimba Temple & Old Manali cafes"], warnings: [] },
        { day: 4, route: "Manali Solang Valley", tagline: "Snow Activities", intensity: "Moderate", transitHours: "3 hrs", distanceKm: "50 km", meals: "Breakfast & Dinner", activities: ["Solang Valley snow adventures", "Atal Tunnel & Sissu Village visit", "Music party at hotel"], warnings: ["⚠️ Verify Bonfire inclusion for HP003 tier"] },
        { day: 5, route: "Manali to Kangra", tagline: "Tea Gardens & Temples", intensity: "Moderate", transitHours: "6 hrs", distanceKm: "215 km", meals: "Breakfast & Dinner", activities: ["Kullu Rafting & Paragliding stops", "Drive through scenic tea estates", "Overnight stay in Kangra"], warnings: ["⚠️ Adventure sports at own cost"] },
        { day: 6, route: "Kangra to Dalhousie", tagline: "Dharamshala & HPCA", intensity: "Moderate", transitHours: "4 hrs", distanceKm: "120 km", meals: "Breakfast & Dinner", activities: ["HPCA Stadium Dharamshala", "BhagsuNag Waterfall & Dalai Lama Temple", "Evening reach Dalhousie"], warnings: [] },
        { day: 7, route: "Dalhousie & Khajjiar", tagline: "Mini Switzerland", intensity: "Low", transitHours: "Local", distanceKm: "45 km", meals: "Breakfast & Dinner", activities: ["Khajjiar Lake & pine meadow walk", "St. Johns Church & Gandhi Chowk", "Chamunda Devi Temple Aarti"], warnings: [] },
        { day: 8, route: "Dalhousie to Amritsar", tagline: "Wagah Border & Golden Temple", intensity: "High", transitHours: "5 hrs", distanceKm: "200 km", meals: "Breakfast & Langar Dinner", activities: ["Drive to Amritsar", "Wagah Border retreat ceremony", "Golden Temple night illumination & Langar dinner", "Late night departure to Delhi"], warnings: [] },
        { day: 9, route: "Delhi Arrival", tagline: "Trip Concludes", intensity: "Low", transitHours: "Morning", distanceKm: "0 km", meals: "None", activities: ["Morning arrival in Delhi"], warnings: [] }
      ],

      trustInsights: {
        score: 90,
        totalReviews: 198,
        sentiment: { positive: 88, neutral: 9, negative: 3 },
        aspects: [
          { name: "Hotels", icon: "🏨", score: "4.7 / 5", sentimentType: "positive", positives: ["Great properties in Khajjiar and Dalhousie", "Excellent food"], concern: "Kangra hotel was basic" },
          { name: "Cab & Route", icon: "🚗", score: "4.8 / 5", sentimentType: "positive", positives: ["Smooth 9-day driving with expert driver", "Clean Innova vehicle"], concern: "Long travel day on Day 8" }
        ],
        reviewsList: [
          { name: "Ananya D.", rating: 5.0, date: "Aug 2026", comment: "Thrillophilia's 9-day itinerary covers everything! Khajjiar and Golden Temple in one trip was incredible." },
          { name: "Siddharth K.", rating: 4.7, date: "Jul 2026", comment: "Super organized! Drivers were punctual and hotel locations were top-notch." }
        ]
      }
    },

    {
      id: "hp004",
      packageCode: "HP004",
      title: "Classic Shimla & Manali Mountain Retreat",
      subtitle: "Unrushed Hill Station Staying with Included Bonfire Party",
      agency: "EaseMyTrip",
      agencyType: "Verified Niche Travel Partner",
      agencyRating: 4.6,
      sourceUrl: "https://www.easemytrip.com/holidays/hp004-classic-shimla-manali",
      price: 18900,
      originalPrice: 22500,
      duration: "7 Days / 6 Nights",
      durationDays: 7,
      durationNights: 6,
      destination: "Himachal (Shimla/Manali)",
      origin: "Delhi",
      hotel: "3★ Deluxe Shimla & Manali Pine View Resort",
      hotelName: "Pine Wood Villa & Solang Valley Heights",
      hotelRating: 4.6,
      image: "assets/hero-himachal.jpg",
      fitScore: 94,
      valueScore: 92,
      itineraryScore: 91,
      trustScore: 89,
      rating: 4.6,
      totalReviews: 86,
      badge: "BEST RELAXED VALUE",
      badgeIcon: "☕",
      badgeExplanation: "No overnight night travel! Includes comfortable overnight stays in Shimla before driving to Manali.",
      summary: "Relaxed 7-day tour with overnight hotel stay in Shimla (no night bus transit), enroute Pandoh Dam, Solang Valley, and Old Manali cafe exploration.",

      overview: {
        durationText: "7 Days / 6 Nights",
        travelersText: "2 Travelers",
        startingCity: "Starting from Delhi",
        focusText: "Relaxed Leisure Stays",
        paceText: "Unrushed & Comfortable"
      },

      whyMatches: {
        fitPercent: 94,
        reasons: [
          { text: "Right inside your ₹12,000–₹22,000 budget (₹18,900)", positive: true },
          { text: "Zero night bus drives — includes overnight hotel stay in Shimla", positive: true },
          { text: "Explicitly includes Bonfire & Music party in Manali", positive: true },
          { text: "Visit Pandoh Dam, Jogini Waterfalls, and Old Manali Cafes", positive: true },
          { text: "7 days gives ample time to relax without rushing", positive: true }
        ]
      },

      costBreakdown: {
        packagePrice: 18900,
        estimatedAdditional: 1300,
        effectiveTotal: 20200,
        explanation: "Effective Total includes package cost plus local shopping and optional adventure tickets.",
        items: [
          { label: "Advertised Base Price (EaseMyTrip)", amount: 18900, type: "base" },
          { label: "Kullu rafting & photo stops", amount: 600, type: "additional" },
          { label: "Old Manali cafe dining & shopping", amount: 500, type: "additional" },
          { label: "Toll taxes & driver bata", amount: 200, type: "additional" }
        ]
      },

      inclusions: [
        "6 nights stay (2 nights Shimla + 4 nights Manali)",
        "Daily Breakfast & Dinner at all hotels",
        "Private AC Sedan cab for entire 7-day trip from Delhi",
        "Solang Valley, Atal Tunnel, Pandoh Dam & Kufri sightseeing",
        "Bonfire & DJ Music Party night included",
        "All toll, state tax, and driver charges"
      ],

      exclusions: [
        "Rohtang Pass NGT permits & taxi fees",
        "Personal expenses & heater charges",
        "Lunch meals"
      ],

      itinerary: [
        { day: 1, route: "Delhi to Shimla", tagline: "Day Drive to Shimla", intensity: "Low", transitHours: "8 hrs", distanceKm: "340 km", meals: "Dinner", activities: ["Morning departure from Delhi", "Check-in at Shimla resort & leisure evening"], warnings: [] },
        { day: 2, route: "Shimla & Kufri Excursion", tagline: "Ridge & Heritage Walk", intensity: "Low", transitHours: "Local", distanceKm: "40 km", meals: "Breakfast & Dinner", activities: ["Kufri excursion & Green Valley", "Mall Road, Scandal Point & Jakhoo Temple", "Overnight stay in Shimla (no night travel)"], warnings: [] },
        { day: 3, route: "Shimla to Manali via Pandoh Dam", tagline: "Riverside Drive", intensity: "Moderate", transitHours: "7 hrs", distanceKm: "250 km", meals: "Breakfast & Dinner", activities: ["Drive through Mandi valley", "Enroute photo stop at Pandoh Dam", "Check-in Manali"], warnings: [] },
        { day: 4, route: "Solang Valley & Atal Tunnel", tagline: "Snow Peaks & Party", intensity: "Moderate", transitHours: "3 hrs", distanceKm: "50 km", meals: "Breakfast & Dinner", activities: ["Solang Valley views & snow points", "Atal Tunnel drive", "Bonfire & Music party at resort"], warnings: [] },
        { day: 5, route: "Manali Local & Old Manali Cafes", tagline: "Cafes & Jogini Trek", intensity: "Low", transitHours: "Local", distanceKm: "25 km", meals: "Breakfast & Dinner", activities: ["Jogini Waterfall trek & Vashisht hot springs", "Hadimba Temple & Van Vihar", "Old Manali Cafe hopping"], warnings: [] },
        { day: 6, route: "Manali to Delhi", tagline: "Kullu Rafting & Return", intensity: "High", transitHours: "Overnight drive", distanceKm: "530 km", meals: "Breakfast", activities: ["Kullu rafting point visit", "Pandoh Dam stop", "Evening proceed to Delhi"], warnings: [] },
        { day: 7, route: "Delhi Arrival", tagline: "Trip Concludes", intensity: "Low", transitHours: "Morning", distanceKm: "0 km", meals: "None", activities: ["Morning arrival in Delhi"], warnings: [] }
      ],

      trustInsights: {
        score: 89,
        totalReviews: 86,
        sentiment: { positive: 86, neutral: 10, negative: 4 },
        aspects: [
          { name: "Hotels", icon: "🏨", score: "4.6 / 5", sentimentType: "positive", positives: ["Loved staying overnight in Shimla without rushing", "Resort views in Manali were stunning"] },
          { name: "Driver & Support", icon: "🚗", score: "4.7 / 5", sentimentType: "positive", positives: ["EaseMyTrip driver was very courteous", "Punctual transfers"] }
        ],
        reviewsList: [
          { name: "Megha T.", rating: 4.8, date: "Aug 2026", comment: "Having a proper hotel night in Shimla instead of a night bus made all the difference. Super relaxed!" },
          { name: "Karan B.", rating: 4.5, date: "Jul 2026", comment: "Great package by EaseMyTrip. Bonfire night was fun and drivers were very helpful." }
        ]
      }
    },

    {
      id: "hp007",
      packageCode: "HP007",
      title: "Shimla, Manali & Chandigarh Rock Garden Tour",
      subtitle: "Himalayan Vistas paired with Chandigarh Urban Elegance",
      agency: "TravelTriangle Partner",
      agencyType: "Verified Niche Specialist",
      agencyRating: 4.6,
      sourceUrl: "https://traveltriangle.com/packages/hp007-shimla-manali-chandigarh",
      price: 21200,
      originalPrice: 24800,
      duration: "7 Days / 6 Nights",
      durationDays: 7,
      durationNights: 6,
      destination: "Himachal (Shimla/Manali)",
      origin: "Delhi",
      hotel: "3★ Valley View & City Center Hotels",
      hotelName: "Shimla Heights & Chandigarh Central",
      hotelRating: 4.6,
      image: "assets/hero-himachal.jpg",
      fitScore: 93,
      valueScore: 91,
      itineraryScore: 90,
      trustScore: 88,
      rating: 4.6,
      totalReviews: 112,
      badge: "BALANCED CIRCUIT",
      badgeIcon: "🏙️",
      badgeExplanation: "Combines snow peaks of Solang with Chandigarh Rock Garden & Sukhna Lake.",
      summary: "7-day package from Delhi visiting Kufri, Viceregal Lodge, Solang Valley, Kullu valley, Rock Garden, and Sukhna Lake.",

      overview: { durationText: "7 Days / 6 Nights", travelersText: "2 Travelers", startingCity: "Starting from Delhi", focusText: "Hills & Chandigarh", paceText: "Balanced" },
      whyMatches: {
        fitPercent: 93,
        reasons: [
          { text: "Well within your ₹12,000–₹22,000 budget (₹21,200)", positive: true },
          { text: "Includes Chandigarh Rock Garden & Sukhna Lake visit", positive: true },
          { text: "Covers Kufri, Viceregal Lodge & Solang Valley views", positive: true },
          { text: "Includes 6 breakfasts and 6 dinners", positive: true }
        ]
      },
      costBreakdown: { packagePrice: 21200, estimatedAdditional: 1400, effectiveTotal: 22600, items: [{ label: "Base Package Price (TravelTriangle)", amount: 21200, type: "base" }, { label: "Rock Garden & cable car entry tickets", amount: 600, type: "additional" }, { label: "Local snacks & driver bata", amount: 800, type: "additional" }] },
      inclusions: ["6 nights accommodation", "Daily Breakfast & Dinner", "Private cab for entire circuit", "Rock Garden & Kufri sightseeing", "Tolls & parking"],
      exclusions: ["Optional paragliding & pony rides", "Rohtang Pass NGT taxi fee", "Lunch meals"],
      itinerary: [
        { day: 1, route: "Delhi to Shimla", tagline: "Drive to Shimla", intensity: "Low", transitHours: "8 hrs", distanceKm: "340 km", meals: "Dinner", activities: ["Drive to Shimla", "Check-in & evening leisure"], warnings: [] },
        { day: 2, route: "Shimla & Kufri", tagline: "Viceregal Lodge & Kufri", intensity: "Moderate", transitHours: "Local", distanceKm: "45 km", meals: "Breakfast & Dinner", activities: ["Kufri excursion", "Viceregal Lodge, Christ Church & Gaiety Theatre"], warnings: [] },
        { day: 3, route: "Shimla to Manali", tagline: "Kullu Valley Transit", intensity: "Moderate", transitHours: "7 hrs", distanceKm: "250 km", meals: "Breakfast & Dinner", activities: ["Drive via Kullu valley", "Evening market shopping"], warnings: [] },
        { day: 4, route: "Manali Local", tagline: "Temples & Waterfalls", intensity: "Low", transitHours: "Local", distanceKm: "30 km", meals: "Breakfast & Dinner", activities: ["Hadimba Temple, Manu Temple & Vashisht Bath"], warnings: [] },
        { day: 5, route: "Solang Valley", tagline: "Snow Point Views", intensity: "Moderate", transitHours: "3 hrs", distanceKm: "50 km", meals: "Breakfast & Dinner", activities: ["Solang Valley adventure activities", "Evening Mall Road"], warnings: [] },
        { day: 6, route: "Manali to Chandigarh", tagline: "Rock Garden Visit", intensity: "Moderate", transitHours: "8 hrs", distanceKm: "300 km", meals: "Breakfast & Dinner", activities: ["Drive to Chandigarh", "Rock Garden & Sukhna Lake"], warnings: [] },
        { day: 7, route: "Chandigarh to Delhi", tagline: "Return Journey", intensity: "Low", transitHours: "5 hrs", distanceKm: "250 km", meals: "Breakfast", activities: ["Drive back to Delhi"], warnings: [] }
      ],
      trustInsights: {
        score: 88,
        totalReviews: 112,
        sentiment: { positive: 85, neutral: 10, negative: 5 },
        aspects: [{ name: "Hotels", icon: "🏨", score: "4.5 / 5", sentimentType: "positive", positives: ["Chandigarh hotel was modern and clean"] }],
        reviewsList: [{ name: "Pooja V.", rating: 4.7, date: "Aug 2026", comment: "Great trip combination! Loved visiting both mountains and Chandigarh city." }]
      }
    },

    {
      id: "hp013",
      packageCode: "HP013",
      title: "Offbeat Jibhi Valley & Classic Himachal Circuit",
      subtitle: "Discover Waterfall Trails, Jibhi Cabins & Mountain Rivers",
      agency: "KingHills Travels",
      agencyType: "Independent Niche Agency",
      agencyRating: 4.9,
      sourceUrl: "https://kinghillstravels.com/packages/hp013-shimla-manali-jibhi",
      price: 21800,
      originalPrice: 25000,
      duration: "7 Days / 6 Nights",
      durationDays: 7,
      durationNights: 6,
      destination: "Himachal (Shimla/Manali)",
      origin: "Delhi",
      hotel: "3★ Mountain Resorts & Jibhi Eco-Cabins",
      hotelName: "Jibhi Pine Woods & Manali Haven",
      hotelRating: 4.9,
      image: "assets/hero-himachal.jpg",
      fitScore: 95,
      valueScore: 93,
      itineraryScore: 95,
      trustScore: 93,
      rating: 4.9,
      totalReviews: 156,
      badge: "OFFBEAT GEM",
      badgeIcon: "🌲",
      badgeExplanation: "Includes 1 night stay in offbeat Jibhi valley with natural waterfall trail exploration.",
      summary: "Escape the crowds with 7 days exploring Shimla, Solang Valley, Naggar Valley, and serene wooden cabins in Jibhi.",

      overview: { durationText: "7 Days / 6 Nights", travelersText: "2 Travelers", startingCity: "Starting from Delhi", focusText: "Offbeat Valleys & Nature", paceText: "Relaxed & Scenic" },
      whyMatches: {
        fitPercent: 95,
        reasons: [
          { text: "Within your budget at ₹21,800 for 7 full days", positive: true },
          { text: "Includes offbeat stay in Jibhi valley with waterfall trek", positive: true },
          { text: "Covers Naggar Valley & Solang Valley viewpoints", positive: true },
          { text: "Rated 4.9★ by travelers for serene stay experience", positive: true }
        ]
      },
      costBreakdown: { packagePrice: 21800, estimatedAdditional: 1200, effectiveTotal: 23000, items: [{ label: "Base Price (KingHills Travels)", amount: 21800, type: "base" }, { label: "Jibhi waterfall local guide", amount: 400, type: "additional" }, { label: "Optional adventure activities", amount: 800, type: "additional" }] },
      inclusions: ["6 nights stay including Jibhi cabin stay", "Daily Breakfast & Dinner", "Private cab transfers", "Jibhi waterfall excursion", "Tolls & parking"],
      exclusions: ["Trekking guide for deep trails beyond permitted drop", "Rohtang Pass NGT taxi fee", "Lunch meals"],
      itinerary: [
        { day: 1, route: "Delhi to Shimla", tagline: "Drive to Shimla", intensity: "Low", transitHours: "8 hrs", distanceKm: "340 km", meals: "Dinner", activities: ["Drive to Shimla", "Check-in"], warnings: [] },
        { day: 2, route: "Shimla Sightseeing", tagline: "Kufri & Ridge", intensity: "Moderate", transitHours: "Local", distanceKm: "40 km", meals: "Breakfast & Dinner", activities: ["Kufri excursion", "Gaiety Theatre, Scandal Point & Mall Road"], warnings: [] },
        { day: 3, route: "Shimla to Manali", tagline: "Scenic Transit", intensity: "Moderate", transitHours: "7 hrs", distanceKm: "250 km", meals: "Breakfast & Dinner", activities: ["Drive to Manali", "Check-in"], warnings: [] },
        { day: 4, route: "Solang Valley", tagline: "Snow Points", intensity: "Moderate", transitHours: "3 hrs", distanceKm: "50 km", meals: "Breakfast & Dinner", activities: ["Solang Valley activities"], warnings: [] },
        { day: 5, route: "Manali & Naggar Valley", tagline: "Naggar Castle", intensity: "Low", transitHours: "Local", distanceKm: "35 km", meals: "Breakfast & Dinner", activities: ["Hadimba Temple, Vashisht Bath, Naggar Castle"], warnings: [] },
        { day: 6, route: "Manali to Jibhi", tagline: "Jibhi Waterfalls & Pines", intensity: "Low", transitHours: "3 hrs", distanceKm: "100 km", meals: "Breakfast & Dinner", activities: ["Drive to Jibhi", "Explore Jibhi waterfall & wooden cabins"], warnings: ["⚠️ Trekking beyond permit drop at own cost"] },
        { day: 7, route: "Jibhi to Delhi", tagline: "Return Journey", intensity: "High", transitHours: "10 hrs", distanceKm: "490 km", meals: "Breakfast", activities: ["Drive back to Delhi"], warnings: [] }
      ],
      trustInsights: {
        score: 93,
        totalReviews: 156,
        sentiment: { positive: 92, neutral: 6, negative: 2 },
        aspects: [{ name: "Jibhi Stay", icon: "🏡", score: "4.9 / 5", sentimentType: "positive", positives: ["Jibhi eco-cabin was magical surrounded by pine trees"] }],
        reviewsList: [{ name: "Rohan N.", rating: 5.0, date: "Aug 2026", comment: "Jibhi was the best part of the trip! KingHills Travels selected an amazing stay." }]
      }
    },

    {
      id: "hp014",
      packageCode: "HP014",
      title: "Grand Himalayan Panorama with Khajjiar Mini-Switzerland",
      subtitle: "The Ultimate 9-Day Journey across Shimla, Manali, Dharamshala & Dalhousie",
      agency: "Himalayan Heritage",
      agencyType: "Independent Niche Specialist",
      agencyRating: 4.8,
      sourceUrl: "https://himalayanheritage.com/packages/hp014-mini-switzerland-himachal",
      price: 30800,
      originalPrice: 35000,
      duration: "9 Days / 8 Nights",
      durationDays: 9,
      durationNights: 8,
      destination: "Himachal (Shimla/Manali)",
      origin: "Delhi",
      hotel: "4★ Heritage & Mountain Resorts",
      hotelName: "Grand Heritage Shimla & Khajjiar Pines",
      hotelRating: 4.8,
      image: "assets/hero-himachal.jpg",
      fitScore: 91,
      valueScore: 89,
      itineraryScore: 96,
      trustScore: 92,
      rating: 4.8,
      totalReviews: 230,
      badge: "LUXURY CIRCUIT",
      badgeIcon: "🏔️",
      badgeExplanation: "Comprehensive 9-day luxury tour covering Khajjiar Mini Switzerland, Dharamshala & Shimla.",
      summary: "9-day premium circuit covering Kufri, Solang Valley, Palampur tea estates, Dalai Lama Temple Dharamshala, and Khajjiar Lake.",

      overview: { durationText: "9 Days / 8 Nights", travelersText: "2 Travelers", startingCity: "Starting from Delhi", focusText: "Heritage & Nature", paceText: "Unrushed & Comprehensive" },
      whyMatches: {
        fitPercent: 91,
        reasons: [
          { text: "AI Recommendation: Over budget range by ₹8,800, but delivers 4★ heritage hotels & 9 days full Himachal coverage", positive: true },
          { text: "Includes overnight stay in Khajjiar ('Mini Switzerland')", positive: true },
          { text: "Covers Palampur tea gardens & McLeod Ganj", positive: true }
        ]
      },
      costBreakdown: { packagePrice: 30800, estimatedAdditional: 1600, effectiveTotal: 32400, items: [{ label: "Base Price (Himalayan Heritage)", amount: 30800, type: "base" }, { label: "Palampur tea tasting & local entries", amount: 600, type: "additional" }, { label: "Driver bata & parking", amount: 1000, type: "additional" }] },
      inclusions: ["8 nights in 4★ handpicked hotels", "Daily Breakfast & Dinner", "Private SUV cab", "Khajjiar lake & Dharamshala tours", "All taxes"],
      exclusions: ["Rohtang Pass NGT taxi", "Personal expenses"],
      itinerary: [
        { day: 1, route: "Delhi to Shimla", tagline: "Drive to Shimla", intensity: "Low", transitHours: "8 hrs", distanceKm: "340 km", meals: "Dinner", activities: ["Drive to Shimla", "Check-in"], warnings: [] },
        { day: 2, route: "Shimla & Kufri", tagline: "Heritage & Peaks", intensity: "Moderate", transitHours: "Local", distanceKm: "40 km", meals: "Breakfast & Dinner", activities: ["Kufri excursion", "Viceregal Lodge, Christ Church"], warnings: [] },
        { day: 3, route: "Shimla to Manali", tagline: "Valley Drive", intensity: "Moderate", transitHours: "7 hrs", distanceKm: "250 km", meals: "Breakfast & Dinner", activities: ["Drive to Manali", "Check-in"], warnings: [] },
        { day: 4, route: "Solang Valley", tagline: "Snow Views", intensity: "Moderate", transitHours: "3 hrs", distanceKm: "50 km", meals: "Breakfast & Dinner", activities: ["Solang Valley activities"], warnings: [] },
        { day: 5, route: "Manali Local", tagline: "Temples & Naggar", intensity: "Low", transitHours: "Local", distanceKm: "30 km", meals: "Breakfast & Dinner", activities: ["Hadimba Temple, Vashisht Bath, Naggar Valley"], warnings: [] },
        { day: 6, route: "Manali to Dharamshala", tagline: "Palampur Tea Gardens", intensity: "Moderate", transitHours: "7 hrs", distanceKm: "230 km", meals: "Breakfast & Dinner", activities: ["Drive via Baijnath Temple & Palampur tea estates"], warnings: [] },
        { day: 7, route: "Dharamshala to Dalhousie", tagline: "McLeod Ganj & Waterfalls", intensity: "Moderate", transitHours: "4 hrs", distanceKm: "120 km", meals: "Breakfast & Dinner", activities: ["Dalai Lama Temple, Bhagsunag Falls, Panjpulla"], warnings: [] },
        { day: 8, route: "Khajjiar Excursion", tagline: "Mini Switzerland of India", intensity: "Low", transitHours: "Local", distanceKm: "30 km", meals: "Breakfast & Dinner", activities: ["Khajjiar Lake & meadow stroll", "Overnight stay in Khajjiar"], warnings: [] },
        { day: 9, route: "Dalhousie to Delhi", tagline: "Return Journey", intensity: "High", transitHours: "11 hrs", distanceKm: "560 km", meals: "Breakfast", activities: ["Drive back to Delhi"], warnings: [] }
      ],
      trustInsights: {
        score: 92,
        totalReviews: 230,
        sentiment: { positive: 91, neutral: 7, negative: 2 },
        aspects: [{ name: "Heritage Stay", icon: "🏰", score: "4.9 / 5", sentimentType: "positive", positives: ["Khajjiar resort had panoramic valley views"] }],
        reviewsList: [{ name: "Suresh P.", rating: 5.0, date: "Aug 2026", comment: "Himalayan Heritage delivered a 5-star experience! Worth every rupee." }]
      }
    },

    {
      id: "ke001",
      packageCode: "KE001",
      title: "Munnar Tea Plantations & Periyar Spice Trails",
      subtitle: "Misty Mountains, Organic Spice Farms & Wildlife Sanctuaries",
      agency: "Kerala Niche Escapes",
      agencyType: "Independent Local Agency",
      agencyRating: 4.8,
      sourceUrl: "https://keralanicheescapes.com/packages/ke001-munnar-thekkady",
      price: 24500,
      originalPrice: 28000,
      duration: "5 Days / 4 Nights",
      durationDays: 5,
      durationNights: 4,
      destination: "Kerala",
      origin: "Kochi",
      hotel: "3★ Nature Resort in Munnar Valley",
      hotelName: "Elysium Mist Valley Nature Resort",
      hotelRating: 4.8,
      image: "assets/munnar-thekkady.jpg",
      fitScore: 90,
      valueScore: 88,
      itineraryScore: 90,
      trustScore: 88,
      rating: 4.8,
      totalReviews: 148,
      badge: "KERALA FAVORITE",
      badgeIcon: "🌿",
      badgeExplanation: "Best balance of nature, tea estates, spice plantations, and relaxed pace in Kerala.",
      summary: "Experience the cool mist of Munnar's endless tea gardens paired with the rich flora and spice hills of Thekkady.",

      overview: { durationText: "5 Days / 4 Nights", travelersText: "2 Travelers", startingCity: "Starting from Kochi", focusText: "Nature & Tea Estates", paceText: "Relaxed" },
      whyMatches: {
        fitPercent: 90,
        reasons: [
          { text: "Within your budget range at ₹24,500", positive: true },
          { text: "Strong nature experiences (Tea plantations, spice gardens, wildlife trails)", positive: true },
          { text: "Relaxed itinerary with 3–5 hours of free time daily", positive: true }
        ]
      },
      costBreakdown: { packagePrice: 24500, estimatedAdditional: 1500, effectiveTotal: 26000, items: [{ label: "Base Price (Kerala Niche Escapes)", amount: 24500, type: "base" }, { label: "Spice garden & tea museum entry fees", amount: 650, type: "additional" }, { label: "Local lunches & driver bata", amount: 850, type: "additional" }] },
      inclusions: ["4 nights stay in 3★ Nature Resort", "Daily Breakfast buffet", "Private AC sedan cab for 5 days", "Guided spice plantation walk", "Tolls & parking"],
      exclusions: ["Airfare or train fares to Kochi", "Periyar lake boat cruise ticket", "Lunches & dinners"],
      itinerary: [
        { day: 1, route: "Kochi to Munnar", tagline: "Ascent through Waterfalls", intensity: "Moderate", transitHours: "4 hrs", distanceKm: "130 km", meals: "Breakfast", activities: ["Pick up from Kochi airport/railway station", "Cheeyappara & Valara waterfall photo stops", "Check-in at Munnar Nature Resort"], warnings: [] },
        { day: 2, route: "Munnar Tea Gardens", tagline: "Misty Tea Estates", intensity: "Low", transitHours: "Local", distanceKm: "35 km", meals: "Breakfast", activities: ["Eravikulam National Park (Nilgiri Tahr)", "Lockhart Tea Museum & artisanal tea tasting"], warnings: ["⚠️ Tea Museum closed on Mondays"] },
        { day: 3, route: "Munnar to Thekkady", tagline: "Spice Hills Drive", intensity: "Moderate", transitHours: "3 hrs", distanceKm: "90 km", meals: "Breakfast", activities: ["Scenic hillside drive to Thekkady", "Guided organic spice plantation walk", "Kumily handicraft market walk"], warnings: [] },
        { day: 4, route: "Thekkady Sanctuary", tagline: "Periyar Wildlife", intensity: "Low", transitHours: "Local", distanceKm: "20 km", meals: "Breakfast", activities: ["Periyar Tiger Reserve buffer zone walk", "Optional Periyar lake boat cruise"], warnings: [] },
        { day: 5, route: "Thekkady to Kovalam / Kochi", tagline: "Departure Transfer", intensity: "Moderate", transitHours: "4 hrs", distanceKm: "160 km", meals: "Breakfast", activities: ["Breakfast & checkout", "Transfer to Kochi/Trivandrum for onward journey"], warnings: [] }
      ],
      trustInsights: {
        score: 88,
        totalReviews: 148,
        sentiment: { positive: 88, neutral: 9, negative: 3 },
        aspects: [{ name: "Resort Stay", icon: "🏨", score: "4.8 / 5", sentimentType: "positive", positives: ["Beautiful balcony view over cardamom plantations"] }],
        reviewsList: [{ name: "Deepak S.", rating: 4.9, date: "Aug 2026", comment: "Kerala Niche Escapes provided a tranquil holiday! Drivers were smooth and polite." }]
      }
    }
  ],

  comparisonMetrics: [
    { key: "price", label: "Package Base Price", format: (v) => `₹${v.toLocaleString('en-IN')}` },
    { key: "effectiveCost", label: "Effective Total Cost", format: (v) => `₹${v.toLocaleString('en-IN')}` },
    { key: "agency", label: "Provider Agency", format: (v) => v },
    { key: "fitScore", label: "AI Fit Match", format: (v) => `${v}%` },
    { key: "rating", label: "Customer Rating", format: (v) => `⭐ ${v} / 5` },
    { key: "trustScore", label: "Trust Score", format: (v) => `${v} / 100` },
    { key: "hotel", label: "Hotel Category", format: (v) => v },
    { key: "duration", label: "Duration", format: (v) => v },
    { key: "pace", label: "Pacing & Style", format: (v) => v }
  ]
};

if (typeof window !== "undefined") {
  window.TRIPWISE_DATA = TRIPWISE_DATA;
}
