import {
  BarChart,
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  LineChart,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
} from "cursor/canvas";

const weeklyGmvShare = [
  { w: "22 чер", share: 17.15 },
  { w: "29 чер", share: 16.38 },
  { w: "06 лип", share: 16.18 },
  { w: "13 лип", share: 16.01 },
  { w: "20 лип", share: 15.8 },
  { w: "27 лип", share: 15.02 },
  { w: "03 сер", share: 14.36 },
  { w: "10 сер", share: 13.93 },
  { w: "17 сер", share: 15.6 },
];

const segmentMargin = [
  { segment: "SMB", margin: 2.54, tone: "success" as const },
  { segment: "Mid-market", margin: 1.89, tone: "success" as const },
  { segment: "McDonald's", margin: 0.07, tone: "warning" as const },
  { segment: "KFC", margin: -0.26, tone: "danger" as const },
];

export default function BoltPlusQ4GrowthStrategy() {
  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <Row gap={8} align="center">
          <H1>Bolt+ Q4: план росту частки GMV в Україні</H1>
          <Pill tone="info" active>
            Окремо від MOV-кейсу
          </Pill>
        </Row>
        <Text tone="secondary">
          Запит Viacheslav Levchenko: не одна кампанія, а система з чотирьох
          двигунів — Visa/банки, SMB/MM, McD/KFC commercial reset і Marketing.
          Ціль Q4: підняти частку обороту від підписників Bolt+ з ~15,5% до
          19–20%, одночасно покращивши mix партнерів і економіку.
        </Text>
      </Stack>

      <Callout tone="info" title="Головна думка">
        Merchant coverage уже ~78% — це не головний bottleneck. Проблема в
        acquisition, activation і mix: McD+KFC дають ~42% Plus-замовлень, але
        margin proxy на замовлення там €0,07 і −€0,26. SMB/MM дають €2,54 і
        €1,89. Q4 = партнер оплачує acquisition (Visa), локальні партнери
        активують прибутковий selection (SMB/MM), McD/KFC або інвестують, або
        не отримують додаткових субсидій, а Marketing масштабує вже готову
        цінність — не порожню підписку.
      </Callout>

      <H2>1. Baseline і target bridge</H2>
      <Text tone="secondary">
        <Pill tone="success" active>
          DBX fact
        </Pill>{" "}
        Джерела: fact_delivery_country_weekly, fact_order_delivery,
        fact_user_subscriptions · UA · food + 3P stores · червень–серпень 2026.
      </Text>
      <Grid columns={4} gap={12}>
        <Stat value="15,5%" label="Bolt+ GMV share зараз (avg останніх 8 тиж.)" tone="warning" />
        <Stat value="19,8%" label="GMV share до підвищення MOV (pre 7w)" tone="info" />
        <Stat value="€9,3 млн" label="Загальний GMV / місяць" />
        <Stat value="€93 тис." label="1 п.п. частки ≈ Bolt+ GMV / місяць" />
      </Grid>
      <Grid columns={4} gap={12}>
        <Stat value="~21 тис." label="Plus-замовлень / повний тиждень" />
        <Stat value="~9,5 тис." label="Активних Plus-користувачів / тиждень" />
        <Stat value="1,4–1,6 тис." label="Нових trial / тиждень (базовий темп)" tone="warning" />
        <Stat value="2,24" label="Plus-замовлень на активного користувача / тиждень" />
      </Grid>
      <LineChart
        categories={weeklyGmvShare.map((d) => d.w)}
        series={[
          {
            name: "Частка GMV від Bolt+ (%)",
            data: weeklyGmvShare.map((d) => d.share),
            tone: "warning",
          },
        ]}
        height={220}
        beginAtZero={false}
        referenceLines={[
          { value: 19.8, label: "Pre-MOV 19,8%", tone: "info" },
          { value: 20, label: "Q4 target 20%", tone: "success" },
          { value: 15.5, label: "Baseline 15,5%", tone: "danger" },
        ]}
      />
      <Table
        headers={["Сценарій Q4", "GMV share", "Δ vs baseline", "Plus GMV / місяць", "Що це означає"]}
        columnAlign={["left", "right", "right", "right", "left"]}
        rowTone={["warning", "neutral", "success", "success", "info"]}
        rows={[
          ["Baseline (зараз)", "15,5%", "—", "~€1,44 млн", "Статус-кво без нових двигунів"],
          ["Conservative", "17,5–18%", "+2,0–2,5 п.п.", "~€1,63–1,67 млн", "Visa pilot + обережний SMB uplift"],
          ["Base target", "19–20%", "+3,5–4,5 п.п.", "~€1,77–1,86 млн", "Visa scale + SMB activation + marketing"],
          ["Upside", "21–22%", "+5,5–6,5 п.п.", "~€1,95–2,05 млн", "Усі двигуни + сильний retention"],
        ]}
      />
      <Text size="small" tone="tertiary">
        Gap до 20%: +4,5 п.п. ≈ +€420 тис. Bolt+ GMV на місяць. Не додавати
        ефекти механічно — Visa, Marketing і SMB можуть перетинатися на тих
        самих користувачах.
      </Text>

      <H2>2. Segment economics — чому mix важливий</H2>
      <Text tone="secondary">
        <Pill tone="success" active>
          DBX fact
        </Pill>{" "}
        Direct margin proxy = commission + eater fees − courier − demand
        incentives. Не invoiced CP L2, але коректно для порівняння сегментів ·
        останні ~8,5 тижнів · delivered Plus orders.
      </Text>
      <BarChart
        categories={segmentMargin.map((d) => d.segment)}
        series={[
          {
            name: "Direct margin proxy (€ / Plus order)",
            data: segmentMargin.map((d) => d.margin),
            tone: "info",
          },
        ]}
        height={200}
      />
      <Table
        headers={[
          "Сегмент",
          "Plus orders",
          "Plus GMV penetration",
          "Commission rate",
          "Margin proxy / order",
          "Plus providers enrolled",
        ]}
        columnAlign={["left", "right", "right", "right", "right", "right"]}
        rowTone={["success", "success", "warning", "danger"]}
        rows={[
          ["SMB restaurants", "25 759", "13,9%", "29,3%", "€2,54", "2 512"],
          ["Mid-market", "56 486", "16,3%", "25,8%", "€1,89", "1 839"],
          ["McDonald's", "63 476", "15,9%", "15,0%", "€0,07", "120"],
          ["KFC", "12 538", "15,6%", "15,4%", "−€0,26", "71"],
        ]}
      />
      <Grid columns={3} gap={12}>
        <Stat value="42,1%" label="McD + KFC share of Plus orders" tone="warning" />
        <Stat value="€2,54" label="SMB margin proxy — у 36× вище за McD" tone="success" />
        <Stat value="13,4–16,4%" label="Plus order penetration по сегментах" />
      </Grid>
      <Callout tone="warning" title="Viacheslav position (Slack, 28.04)">
        McD+KFC ≈ 44% GMV, але ~85% Bolt+ orders за 6 міс. — structural
        dependency з поганою UE. Стратегія Q4: не нові преференції для них, а
        commercial reset + shift mix на SMB/MM, де economics кращі.
      </Callout>

      <H2>3. Subscriber value — acquisition math</H2>
      <Text tone="secondary">
        <Pill tone="success" active>
          DBX fact
        </Pill>{" "}
        Cohort value · fact_user_subscriptions + fact_order_delivery · cohorts
        бер–лип 2026.
      </Text>
      <Table
        headers={[
          "Cohort",
          "New subs",
          "Food active 30d",
          "Plus orders / sub (30d)",
          "Plus GMV / sub (30d)",
          "Retained 60d",
        ]}
        columnAlign={["left", "right", "right", "right", "right", "right"]}
        rows={[
          ["Бер 2026", "8 562", "68,7%", "2,67", "€40,69", "24,3%"],
          ["Кві 2026", "9 351", "66,0%", "2,50", "€38,91", "22,5%"],
          ["Тра 2026", "7 742", "61,3%", "2,32", "€36,68", "21,4%"],
          ["Чер 2026", "6 823", "62,2%", "2,62", "€40,51", "11,0%"],
        ]}
      />
      <Grid columns={3} gap={12}>
        <Stat value="~€40" label="Plus GMV / новий sub · перші 30 днів" />
        <Stat value="~62–69%" label="Food activation · 30 днів" tone="info" />
        <Stat value="11–24%" label="Subscription retained · 60 днів" tone="warning" />
      </Grid>
      <Text>
        Робоча оцінка для Visa pilot: новий sub ≈ €40 GMV у перші 30 днів.
        2 000 redeemed codes × €40 ≈ €81 тис. (+0,8–0,9 п.п.). 5 000 × €40 ≈
        €203 тис. (+2,1 п.п.).{" "}
        <Pill tone="warning" active>
          Scenario
        </Pill>
      </Text>

      <Divider />

      <H2>4. Чотири двигуни — stakeholder contract</H2>
      <Table
        headers={["Двигун", "Owner", "Їхній KPI / інтерес", "Їхній внесок", "Bolt+ KPI", "Credit модель"]}
        columnAlign={["left", "left", "left", "left", "left", "left"]}
        rows={[
          [
            "Visa / банки",
            "Artem Havriushyn, Oleksandr Holovnenko",
            "Card usage, new cardholders, brand visibility",
            "80% subsidy, 5–20k codes, bank media",
            "New subs, redemption, 30d activation",
            "Partner-funded subs · не Bolt DI",
          ],
          [
            "SMB / MM",
            "AM / KAM (local)",
            "Incremental orders, visibility, ROAS",
            "Exclusive offers, Ads, co-funded discounts",
            "Plus GMV penetration SMB/MM, margin proxy",
            "Partner GMV + Ads revenue + co-funding",
          ],
          [
            "McD / KFC",
            "Enterprise AM + Viacheslav",
            "Brand traffic without extra cost",
            "+1–1,5% Plus commission OR Ads/co-fund",
            "Stop UE bleed · reinvest €8,5k/mo",
            "Partner investment → acquisition pool",
          ],
          [
            "Marketing / Growth",
            "UA Marketing + Growth",
            "Reach, CAC, campaign ROI",
            "CRM, modals, bank cross-promo, comms",
            "Trials, GMV share, orders/user",
            "Incremental subs at target CAC",
          ],
          [
            "Product",
            "Bolt+ Product + Vengatesh",
            "Campaign compatibility, UX",
            "Deeplink/webview, campaign priority fix",
            "Redemption rate, test validity",
            "Unblock Visa + cashback tests",
          ],
          [
            "Program lead",
            "Yaroslav Bokii",
            "End-to-end delivery, analytics",
            "Scorecard, experiment design, alignment",
            "GMV share + guardrails",
            "North Star owner",
          ],
        ]}
      />
      <Callout tone="info" title="Sponsor">
        Viacheslav Levchenko — executive sponsor, commercial reset authority,
        final call on McD/KFC terms and DI guardrails.
      </Callout>

      <H2>5. Q4 roadmap</H2>
      <Table
        headers={["Фаза", "Коли", "Deliverables", "Exit criteria"]}
        columnAlign={["left", "left", "left", "left"]}
        rows={[
          [
            "Foundation",
            "До кін. серпня",
            "North Star + guardrails, stakeholder contract, campaign calendar, no-comms-before-QA rule",
            "Signed KPI sheet · calendar v1 · Product blockers list",
          ],
          [
            "Visa pilot",
            "Вересень",
            "5k codes · internal QA → 10% soft → scale",
            "Redemption ≥25% · 30d activation ≥55% · CP within guardrail",
          ],
          [
            "SMB/MM activation",
            "Вер–жов",
            "Local Favourites · top pool · Kyiv + holdout cities",
            "SMB Plus penetration +2 pp vs control · margin proxy ↑",
          ],
          [
            "McD/KFC reset",
            "Вер–жов",
            "Economics deck · negotiation · Cyprus precedent",
            "+1–1,5% commission OR equivalent Ads · or no extra subsidy",
          ],
          [
            "Marketing amp",
            "Жов–лист",
            "One story: bank sub + local exclusives",
            "Trial WoW uplift · CAC within target",
          ],
          [
            "Scale / review",
            "Грудень",
            "Weekly scorecard · stop/scale decisions",
            "19–20% base OR documented learnings",
          ],
        ]}
      />

      <H2>6. Experiment roadmap — пілоти з holdouts</H2>

      <H3>6.1 Visa / bank acquisition</H3>
      <Text tone="secondary">
        <Pill tone="success" active>
          Slack fact
        </Pill>{" "}
        80% subsidy negotiated · 5k start codes · scale to 20k · UX/deeplink
        blocker · Visa campaigns can override Plus cashback (no MOV).
      </Text>
      <Table
        headers={["Параметр", "Design", "KPI", "Stop", "Scale"]}
        columnAlign={["left", "left", "left", "left", "left"]}
        rows={[
          [
            "Audience",
            "New + lapsed subs only; exclude active payers",
            "Redemption rate",
            "<15% after 2 weeks",
            "≥30% redemption → add 5k codes",
          ],
          [
            "Holdout",
            "10–20% random · same bank audience",
            "Incremental subs vs holdout",
            "No lift vs holdout at 4 weeks",
            "Lift ≥15% incremental subs",
          ],
          [
            "Rollout",
            "50–100 internal → 10% soft → full",
            "30d food activation, GMV/sub",
            "Activation <45%",
            "Activation ≥55% + CP OK → marketing",
          ],
          [
            "Product",
            "Fix campaign priority vs Visa no-MOV",
            "Cashback + Visa coexistence",
            "Override persists",
            "QA sign-off before external comms",
          ],
        ]}
      />
      <Grid columns={3} gap={12}>
        <Stat value="5k codes" label="Pilot size" />
        <Stat value="40%" label="Redemption assumption → 2k subs" tone="info" />
        <Stat value="+0,8–0,9 п.п." label="GMV share scenario (30d)" tone="success" />
      </Grid>
      <Grid columns={3} gap={12}>
        <Stat value="20k codes" label="Scale scenario" />
        <Stat value="25%" label="Redemption assumption → 5k subs" tone="info" />
        <Stat value="+2,1 п.п." label="GMV share scenario (monthly)" tone="success" />
      </Grid>

      <H3>6.2 SMB / MM — Bolt+ Local Favourites</H3>
      <Table
        headers={["Параметр", "Design", "KPI", "Stop", "Scale"]}
        columnAlign={["left", "left", "left", "left", "left"]}
        rows={[
          [
            "Partner pool",
            "Top enrolled SMB/MM: commission ≥25%, rating, availability, basket 250–400 UAH",
            "Pool size ≥150 providers",
            "<80 qualified partners",
            "Expand to 300+ in 2 cities",
          ],
          [
            "Offer",
            "Exclusive menu/item + partner-funded 10–15% OR Ads bundle",
            "Plus orders / partner, ROAS",
            "ROAS <1 for 4 weeks",
            "ROAS ≥1.5 → national playbook",
          ],
          [
            "Holdout",
            "Matched providers in control city; user holdout 10%",
            "Incremental Plus GMV vs control",
            "No penetration lift",
            "+2 pp penetration → +1 city/week",
          ],
          [
            "Visibility",
            "Bolt+ carousel + Sponsored Listings slot",
            "Click-to-order, mix shift",
            "Mix unchanged 6 weeks",
            "SMB share of Plus orders +3 pp",
          ],
        ]}
      />
      <Text>
        Scenario: SMB/MM Plus penetration 13–16% → 18% ≈ +€27k/week (+1,2 п.п.
        total share). To 20% ≈ +2,2 п.п.{" "}
        <Pill tone="warning" active>
          Scenario — needs holdout
        </Pill>
      </Text>

      <H3>6.3 McDonald's / KFC — commercial reset</H3>
      <Table
        headers={["Параметр", "Design", "KPI", "Stop", "Scale"]}
        columnAlign={["left", "left", "left", "left", "left"]}
        rows={[
          [
            "Ask",
            "+1–1,5% Bolt+ commission OR €8,5k/mo Ads equivalent",
            "Signed term or walk-away",
            "No movement by Oct 31",
            "Reinvest revenue into Visa/SMB pool",
          ],
          [
            "Precedent",
            "McD Cyprus: 0% → 1,5% from Sep",
            "Partner acceptance rate",
            "—",
            "Use in UA negotiation deck",
          ],
          [
            "Fallback",
            "Keep base Plus presence · no new exclusive subsidy",
            "McD/KFC Plus share stable, no DI increase",
            "DI creep for McD/KFC",
            "Redirect marketing inventory to co-funding partners",
          ],
          [
            "Holdout",
            "No holdout — commercial negotiation",
            "Margin proxy McD/KFC",
            "Give extra subsidy without return",
            "Document walk-away terms",
          ],
        ]}
      />

      <H3>6.4 Marketing amplification</H3>
      <Table
        headers={["Параметр", "Design", "KPI", "Stop", "Scale"]}
        columnAlign={["left", "left", "left", "left", "left"]}
        rows={[
          [
            "Timing",
            "Only after Visa QA + SMB offers live",
            "Trial WoW vs 4w pre",
            "Launch before Product QA",
            "WoW trials +20% sustained 3w",
          ],
          [
            "Segments",
            "High-frequency non-subs, lapsed, Plus-ready, bank cohort",
            "CAC per incremental sub",
            "CAC > €12 per incremental sub",
            "Double spend on best segment",
          ],
          [
            "Channels",
            "Bank media, CRM, in-app, Rides cross-promo",
            "Redemption → order funnel",
            "CTR < benchmark −30%",
            "Shift budget to winning channel",
          ],
          [
            "Cashback test",
            "Fix Visa override first (Slack 19.08)",
            "Incremental Plus GMV vs control",
            "No lift at 4 weeks",
            "Scale if ROI > 1.2",
          ],
        ]}
      />

      <H2>7. Target bridge — як збираємо +4,5 п.п.</H2>
      <Text tone="secondary">
        <Pill tone="warning" active>
          Scenario model
        </Pill>{" "}
        Не сумувати сліпо — overlap discount ~20–30%.
      </Text>
      <Table
        headers={["Двигун", "Conservative", "Base", "Upside", "Overlap note"]}
        columnAlign={["left", "right", "right", "right", "left"]}
        rows={[
          ["Visa / bank", "+0,5–0,9 п.п.", "+1,0–2,1 п.п.", "+2,1 п.п.", "Mostly new subs"],
          ["SMB / MM activation", "+0,5–1,2 п.п.", "+1,2–2,2 п.п.", "+2,5 п.п.", "Mix + frequency"],
          ["McD/KFC reinvestment", "+0,2 п.п.", "+0,3–0,5 п.п.", "+0,5 п.п.", "Only if commission signed"],
          ["Marketing + retention", "+0,5–1,0 п.п.", "+1,0–1,5 п.п.", "+2,0 п.п.", "Overlaps Visa/SMB"],
          ["MOV revert (optional)", "—", "+0,5–1,5 п.п.", "+2,0 п.п.", "Separate case · not in Q4 base"],
        ]}
      />

      <H2>8. Guardrails і weekly scorecard</H2>
      <Grid columns={4} gap={12}>
        <Stat value="CP L2" label="North Star guardrail — не погіршувати vs baseline" tone="warning" />
        <Stat value="DI / GMV" label="Ceiling agreed with finance · currently ~7,5%" tone="warning" />
        <Stat value="60d retention" label="Floor ~20% on new cohorts" />
        <Stat value="Partner-funded %" label="Target ↑ each month" tone="success" />
      </Grid>
      <Table
        headers={["Metric", "Frequency", "Owner", "Red flag"]}
        rows={[
          ["Bolt+ GMV share", "Weekly", "Yaroslav", "↓ 2 consecutive weeks post-launch"],
          ["New trials / first subs", "Weekly", "Marketing", "<1,2k/week after amp"],
          ["Visa redemption + activation", "Weekly", "Artem/Oleksandr", "Redemption <20%"],
          ["SMB Plus penetration", "Weekly", "AM/KAM", "Flat vs control 4 weeks"],
          ["Margin proxy by segment", "Bi-weekly", "Yaroslav", "SMB margin ↓ >10%"],
          ["McD/KFC DI share", "Monthly", "Viacheslav", "DI ↑ without partner return"],
          ["Campaign U/C", "Per test", "Growth", "ROI <1 at scale gate"],
        ]}
      />

      <H2>9. Що fact / scenario / hypothesis</H2>
      <Table
        headers={["Тип", "Приклади"]}
        rowTone={["success", "warning", "neutral"]}
        rows={[
          [
            "DBX / Slack fact",
            "GMV share 15,5%; segment margins; 78% enrollment; Visa 80% subsidy; McD Cyprus 1,5%; cashback/Visa override issue",
          ],
          [
            "Scenario (розрахунок)",
            "Visa 2k/5k subs → +0,8–2,1 п.п.; SMB penetration 18% → +1,2 п.п.; McD+KFC +1,5% → €8,5k/mo reinvest",
          ],
          [
            "Hypothesis (треба тест)",
            "Local Favourites підніме SMB share of Plus orders; bank deeplink fix → redemption ≥30%; commercial reset не втратить McD traffic",
          ],
        ]}
      />

      <Divider />

      <H2>10. Повідомлення для Viacheslav — alignment draft</H2>
      <Card>
        <CardHeader>Paste-ready · UA</CardHeader>
        <CardBody>
          <Stack gap={8}>
            <Text>
              Viacheslav, підготував Q4-стратегію росту Bolt+ GMV share окремо
              від MOV-кейсу. Baseline з DBX: ~15,5% share (було 19,8% pre-MOV),
              ~€9,3M total GMV, ~1,4–1,6k new trials/week. Target Q4: 19–20%
              (+€420k Bolt+ GMV/mo).
            </Text>
            <Text>
              Ключовий insight з твоєго квітневого месседжу підтверджується
              даними: McD+KFC = 42% Plus orders, margin proxy €0,07 / −€0,26 vs
              SMB €2,54 / MM €1,89. Тому план — не одна кампанія, а 4 двигуни:
              (1) Visa/bank acquisition — 80% funded, 5k codes, pilot вересень;
              (2) SMB/MM Local Favourites — shift mix на прибутковий selection;
              (3) McD/KFC commercial reset — +1–1,5% commission або walk-away
              без нових субсидій; (4) Marketing — тільки після Product QA.
            </Text>
            <Text>
              Кожен пілот має holdout і stop/scale rules. Scenarios (не
              forecast): Visa pilot +0,8–0,9 п.п., scale to +2,1 п.п.; SMB
              activation +1,2–2,2 п.п.; McD/KFC reinvest ~€8,5k/mo if commission
              signed. Conservative Q4: 17,5–18%; base: 19–20%; upside: 21–22%.
              MOV лишається окремим CVP-важелем — не в base plan.
            </Text>
            <Text>
              Потрібно від тебе: (1) sponsor sign-off на 4-engine model; (2)
              mandate для McD/KFC commercial conversation; (3) DI guardrail
              ceiling для Q4 tests. Можемо пройтись по canvas на 30 хв this week.
            </Text>
          </Stack>
        </CardBody>
      </Card>

      <Card>
        <CardHeader>Paste-ready · EN (for broader alignment)</CardHeader>
        <CardBody>
          <Stack gap={8}>
            <Text>
              Sharing the Q4 Bolt+ growth strategy for Ukraine. North Star: lift
              Plus GMV share from ~15.5% to 19–20% by year-end while improving
              partner mix and economics — separate from the MOV case.
            </Text>
            <Text>
              DBX baseline: ~21k Plus orders/week, ~9.5k active users, ~1.4–1.6k
              new trials/week. Segment economics confirm your April point: McD+KFC
              drive ~42% of Plus orders at €0.07 / −€0.26 margin proxy vs SMB
              €2.54 and Mid-market €1.89. Merchant enrollment (~78%) is no
              longer the bottleneck — activation and mix are.
            </Text>
            <Text>
              Four engines: (1) Visa/bank — 80% funded acquisition, 5k-code
              pilot in September with holdout; (2) SMB/MM Local Favourites —
              partner-funded offers + visibility; (3) McD/KFC commercial reset
              — +1–1.5% Plus commission or no extra subsidy; (4) Marketing
              amplification only after Product QA (Visa deeplink, campaign
              priority fix).
            </Text>
            <Text>
              Each pilot has pre-agreed KPIs and stop/scale criteria. Scenario
              bridge to 20%: Visa +0.8–2.1 pp, SMB +1.2–2.2 pp, reinvestment from
              McD/KFC terms + marketing/retention — with overlap discount, not
              mechanical sum. Weekly scorecard on GMV share, trials, redemption,
              segment margin proxy, DI guardrails.
            </Text>
          </Stack>
        </CardBody>
      </Card>

      <Text size="small" tone="tertiary">
        Підготовлено: Yaroslav Bokii · DBX: fact_delivery_country_weekly,
        fact_order_delivery, fact_user_subscriptions, dim_provider_v2 · Slack:
        Viacheslav 28.04, Tayyiba cashback 06.08, Visa thread 19.08 · MOV canvas
        не змінювався.
      </Text>
    </Stack>
  );
}
