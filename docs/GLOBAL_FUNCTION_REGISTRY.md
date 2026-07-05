# 📚 GLOBAL FUNCTION REGISTRY

> **Bách khoa toàn thư API Nội bộ.** Tự động tạo bởi `global_function_auditor.py`.

Tổng số hàm/phương thức: **984**

## ⚠️ CÁC HÀM CÓ THỂ BỊ TRÙNG LẶP (DUPLICATES)
Cần xem xét gộp chung hoặc refactor:
- `_ai_handler` xuất hiện trong 39 files: LangGraph_Agent_System\projects\nsfw_multimedia_auditor\vision_describer.py, src\factory\nodes\system_designer.py, projects\universal_game_vault\src\scraper.py, LangGraph_Agent_System\projects\ceo_agent\ceo_mind.py, src\factory\nodes\omni_overlord.py, Project\LangGraph_Agent_System\src\base_agent.py, LangGraph_Agent_System\projects\ceo_agent\marketing_intel.py, airdrop_guerrilla\src\automation\executor.py, projects\qa_functional_agent\src\functional_tester.py, src\factory\nodes\remediation_agent.py, projects\jarvis-rpg-assistant\jarvis_core\vision_parser.py, projects\ai_trading_agent\src\binance_executor.py, projects\ai_trading_agent\src\fundamental_fetcher.py, projects\ai_trading_agent\src\analysis_to_social.py, projects\ai_trading_agent\src\analytics.py, projects\auto_affiliate_video\src\script_generator.py, LangGraph_Agent_System\projects\ceo_agent\ceo_morning_routine.py, projects\ai_trading_agent\src\whale_tracker.py, src\factory\nodes\router_agent.py, LangGraph_Agent_System\projects\ceo_agent\admin_simulator.py, projects\godot_translator\core\translator.py, src\factory\nodes\architecture_critic.py, src\factory\nodes\qa_agent.py, LangGraph_Agent_System\projects\nsfw_multimedia_auditor\auditor_agent.py, projects\ai_trading_agent\src\telegram_intelligence.py, LangGraph_Agent_System\projects\sovereign_academy\tutor_agent.py, projects\knowledge_base_agent\src\rag_agent.py, projects\qa_chaos_agent\src\llm_autopsy.py, sillytavern_world_card_generator\src\agents\base_agent.py, universal_game_vault\src\processors\batch_importer.py, src\factory\workflows\daily_health_loop.py, LangGraph_Agent_System\src\scrapers\auto_repair_selector.py, LangGraph_Agent_System\projects\nsfw_multimedia_auditor\narrative_bridge.py, projects\ai_trading_agent\src\langgraph_agent.py, src\factory\nodes\workflow_agent.py
- `_logic_handler` xuất hiện trong 39 files: LangGraph_Agent_System\projects\nsfw_multimedia_auditor\vision_describer.py, src\factory\nodes\system_designer.py, projects\universal_game_vault\src\scraper.py, LangGraph_Agent_System\projects\ceo_agent\ceo_mind.py, src\factory\nodes\omni_overlord.py, Project\LangGraph_Agent_System\src\base_agent.py, LangGraph_Agent_System\projects\ceo_agent\marketing_intel.py, airdrop_guerrilla\src\automation\executor.py, projects\qa_functional_agent\src\functional_tester.py, src\factory\nodes\remediation_agent.py, projects\jarvis-rpg-assistant\jarvis_core\vision_parser.py, projects\ai_trading_agent\src\binance_executor.py, projects\ai_trading_agent\src\fundamental_fetcher.py, projects\ai_trading_agent\src\analysis_to_social.py, projects\ai_trading_agent\src\analytics.py, projects\auto_affiliate_video\src\script_generator.py, LangGraph_Agent_System\projects\ceo_agent\ceo_morning_routine.py, projects\ai_trading_agent\src\whale_tracker.py, src\factory\nodes\router_agent.py, LangGraph_Agent_System\projects\ceo_agent\admin_simulator.py, projects\godot_translator\core\translator.py, src\factory\nodes\architecture_critic.py, src\factory\nodes\qa_agent.py, LangGraph_Agent_System\projects\nsfw_multimedia_auditor\auditor_agent.py, projects\ai_trading_agent\src\telegram_intelligence.py, LangGraph_Agent_System\projects\sovereign_academy\tutor_agent.py, projects\knowledge_base_agent\src\rag_agent.py, projects\qa_chaos_agent\src\llm_autopsy.py, sillytavern_world_card_generator\src\agents\base_agent.py, universal_game_vault\src\processors\batch_importer.py, src\factory\workflows\daily_health_loop.py, LangGraph_Agent_System\src\scrapers\auto_repair_selector.py, LangGraph_Agent_System\projects\nsfw_multimedia_auditor\narrative_bridge.py, projects\ai_trading_agent\src\langgraph_agent.py, src\factory\nodes\workflow_agent.py
- `main` xuất hiện trong 34 files: projects\jarvis-rpg-assistant\src\note_search.py, projects\auto_affiliate_video\src\main.py, projects\jarvis-rpg-assistant\src\bot_evolve.py, LangGraph_Agent_System\projects\sovereign_terminal\daemon.py, FlowNSFW-main\src\flow_nsfw\pseudo_labeler.py, LangGraph_Agent_System\projects\ceo_agent\marketing_intel.py, LangGraph_Agent_System\src\factory\main.py, LangGraph_Agent_System\projects\godot_translator\main_run.py, projects\jarvis-rpg-assistant\src\bot_teacher.py, LangGraph_Agent_System\projects\universal_web_scraper\main.py, LangGraph_Agent_System\projects\sovereign_terminal\main.py, projects\ai_trading_agent\src\whale_alert.py, LangGraph_Agent_System\projects\gemini_cli\main.py, projects\jarvis-rpg-assistant\src\bot_daily.py, projects\jarvis-rpg-assistant\src\note.py, projects\sillytavern_world_card_generator\src\lore_extractor.py, LangGraph_Agent_System\projects\real_estate_prediction\train_model.py, projects\FlowNSFW-main\scripts\demo.py, LangGraph_Agent_System\projects\local_proxy_server\main.py, Project\LangGraph_Agent_System\src\resume_flow.py, projects\ai_trading_agent\src\funding_rate.py, LangGraph_Agent_System\projects\sillytavern_world_card_generator\run_nsfw_writer.py, airdrop_guerrilla\src\modes\full_auto_cli.py, projects\FlowNSFW-main\scripts\eval_multi_res.py, LangGraph_Agent_System\projects\jarvis-rpg-assistant\main.py, projects\jarvis-rpg-assistant\jarvis_core\telegram_webhook.py, projects\ai_trading_agent\src\telegram_intelligence.py, projects\jarvis-rpg-assistant\jarvis_core\setup_calendar.py, projects\ai_trading_agent\backtest\offline_backtest.py, LangGraph_Agent_System\projects\auto_x_bot\main.py, projects\FlowNSFW-main\scripts\infer.py, projects\FlowNSFW-main\scripts\train.py, LangGraph_Agent_System\projects\auto_affiliate_video\main.py, LangGraph_Agent_System\projects\sovereign_academy\main.py
- `forward` xuất hiện trong 13 files: FlowNSFW-main\src\flow_nsfw\temporal_sparse.py, FlowNSFW-main\src\flow_nsfw\model.py, FlowNSFW-main\src\flow_nsfw\encoder_unet.py, FlowNSFW-main\src\flow_nsfw\detection_head.py, FlowNSFW-main\src\flow_nsfw\flow_net.py, FlowNSFW-main\src\flow_nsfw\ssm_backend.py
- `close` xuất hiện trong 3 files: Project\LangGraph_Agent_System\src\database.py, projects\ai_trading_agent\backtest\offline_backtest.py, projects\sovereign_terminal\core\mcp_client.py
- `evaluate_evolution` xuất hiện trong 3 files: projects\jarvis-rpg-assistant\jarvis_core\ai_agent_fixed.py, projects\jarvis-rpg-assistant\jarvis_core\ai_agent.py, Project\LangGraph_Agent_System\core\logic_auditor.py
- `run` xuất hiện trong 3 files: projects\jarvis-rpg-assistant\jarvis_core\telegram_webhook.py, LangGraph_Agent_System\projects\project_manager_sentry\manager_agent.py, projects\asset_audit_taskforce\src\judge_executor.py
- `init_db` xuất hiện trong 3 files: universal_game_vault\src\storage\db_manager.py, projects\jarvis-rpg-assistant\jarvis_core\database.py, airdrop_guerrilla\src\utils\migrate_to_sqlite.py
- `add_vocab` xuất hiện trong 3 files: projects\jarvis-rpg-assistant\jarvis_core\database.py, projects\jarvis-rpg-assistant\src\admin_panel.py
- `_parse_json_response` xuất hiện trong 2 files: sillytavern_world_card_generator\src\agents\base_agent.py, Project\LangGraph_Agent_System\src\base_agent.py
- `execute` xuất hiện trong 2 files: Project\LangGraph_Agent_System\src\base_agent.py, projects\ai_trading_agent\src\whale_tracker.py
- `_init_db` xuất hiện trong 2 files: Project\LangGraph_Agent_System\src\token_tracker.py, projects\jarvis-rpg-assistant\jarvis_core\database.py
- `qa_node` xuất hiện trong 2 files: src\factory\nodes\qa_agent.py, src\factory\nodes\qa_reviewer.py
- `router_node` xuất hiện trong 2 files: src\factory\workflows\software_production.py, src\factory\nodes\router_agent.py
- `_build_graph` xuất hiện trong 2 files: LangGraph_Agent_System\projects\ceo_agent\autonomous_ceo.py, projects\ai_trading_agent\src\langgraph_agent.py
- `reflect_and_learn` xuất hiện trong 2 files: LangGraph_Agent_System\projects\trading_rpg_simulator\trader_hero.py, LangGraph_Agent_System\projects\ceo_agent\ceo_mind.py
- `predict` xuất hiện trong 2 files: LangGraph_Agent_System\projects\real_estate_prediction\app.py, projects\ai_trading_agent\src\ml_prediction.py
- `load_profile` xuất hiện trong 2 files: projects\jarvis-rpg-assistant\src\admin_panel.py, LangGraph_Agent_System\projects\sovereign_academy\main.py
- `save_profile` xuất hiện trong 2 files: projects\jarvis-rpg-assistant\src\admin_panel.py, LangGraph_Agent_System\projects\sovereign_academy\main.py
- `send_telegram_message` xuất hiện trong 2 files: airdrop_guerrilla\src\modes\full_auto_cli.py, LangGraph_Agent_System\projects\sovereign_terminal\daemon.py

---

## 📁 `FlowNSFW-main\src\flow_nsfw\balanced_sampler.py`
### ⚡ `**BalancedBatchSampler**.__init__(self, manifest_path, split, batch_size, shuffle)`
- *Dòng:* 18

### ⚡ `**BalancedBatchSampler**.__iter__(self)`
- *Dòng:* 38

### ⚡ `**BalancedBatchSampler**.__len__(self)`
- *Dòng:* 56

## 📁 `FlowNSFW-main\src\flow_nsfw\data.py`
### ⚡ `**VideoClipDataset**.__getitem__(self, idx)`
- *Dòng:* 77

### ⚡ `**VideoClipDataset**.__init__(self, manifest, clip_len, resolution, split, seed, frame_stride, multi_scale)`
- *Dòng:* 36

### ⚡ `**VideoClipDataset**.__len__(self)`
- *Dòng:* 74

### ⚡ `_read_img(path)`
- *Mô tả:* Read image as RGB uint8, handling AVIF via ffmpeg fallback.
- *Dòng:* 20

## 📁 `FlowNSFW-main\src\flow_nsfw\detection_head.py`
### ⚡ `**_DetectScale**.__init__(self, in_ch, hidden, num_classes)`
- *Dòng:* 83

### ⚡ `**DetectionHead**.__init__(self, feat_chs, hidden, num_classes, sparse, window_size, sparse_threshold)`
- *Dòng:* 113

### ⚡ `**DetectionHead**._apply_sparse(self, detect_fn, feat)`
- *Mô tả:* Apply detection only on foreground windows.  Uses energy-based foreground mask (no learned parameters needed). Falls back to dense detection if foregr...
- *Dòng:* 133

### ⚡ `_compute_foreground_mask(feat, threshold)`
- *Mô tả:* Simple foreground activation mask from feature energy.  Args:     feat: (B, C, H, W) feature map.     threshold: activation energy threshold.  Returns...
- *Dòng:* 24

### ⚡ `_window_mask_regions(mask, window_size, context)`
- *Mô tả:* Identify windows that intersect with the foreground mask.  Args:     mask: (B, 1, H, W) binary mask.     window_size: spatial window size.     context...
- *Dòng:* 42

### ⚡ `**_DetectScale**.forward(self, x)`
- *Mô tả:* Returns (B, 5+nc, H, W) logits.
- *Dòng:* 96

### ⚡ `**DetectionHead**.forward(self, feat_s8, feat_s4, feat_s2, feat_s1)`
- *Mô tả:* Returns per-scale raw detection tensors.  Each value is (B*T, 5+nc, h, w). Decode to boxes via the model.
- *Dòng:* 166

## 📁 `FlowNSFW-main\src\flow_nsfw\encoder_unet.py`
### ⚡ `**UNetEncoder**.__init__(self, in_ch, dim, skip_ratios, bottleneck_ratio)`
- *Dòng:* 21

### ⚡ `_conv_block(in_ch, out_ch, stride)`
- *Dòng:* 7

### ⚡ `**UNetEncoder**.forward(self, x)`
- *Dòng:* 39

## 📁 `FlowNSFW-main\src\flow_nsfw\flow_net.py`
### ⚡ `**_FlowHead**.__init__(self, corr_ch, feat_ch)`
- *Dòng:* 62

### ⚡ `**FlowNet**.__init__(self, dim, radius)`
- *Dòng:* 79

### ⚡ `**RaftFlowNet**.__init__(self, feat_stride, num_flow_updates)`
- *Dòng:* 104

### ⚡ `_build_corr(f1, f2, radius)`
- *Mô tả:* Correlation volume via unfold + batched matmul.  Equivalent to the naive padding+slicing version but ~2-3x faster on GPU because it avoids the Python ...
- *Dòng:* 22

### ⚡ `**_FlowHead**.forward(self, corr, feat)`
- *Dòng:* 72

### ⚡ `**FlowNet**.forward(self, feat)`
- *Dòng:* 85

### ⚡ `**RaftFlowNet**.forward(self, feat, frames)`
- *Dòng:* 114

## 📁 `FlowNSFW-main\src\flow_nsfw\losses.py`
### ⚡ `_ciou_loss(pred_boxes, target_boxes, target_obj)`
- *Mô tả:* CIoU box loss for positive samples.  pred_boxes: dict with cx,cy,w,h each (B*T, fh, fw) target_boxes: (B*T, 5, max_objs)  [cx,cy,w,h,cls]  padded with...
- *Dòng:* 30

### ⚡ `detection_loss(decoded, targets, weights)`
- *Mô tả:* Per-scale detection loss.  Args:     decoded: list of 4 dicts (s8,s4,s2,s1) with cx,cy,w,h,obj,cls.     targets: list of 4 target dicts at correspondi...
- *Dòng:* 45

### ⚡ `flow_consistency_loss(flow_fwd, flow_bwd, weight)`
- *Mô tả:* Forward-backward flow consistency loss.  Args:     flow_fwd: (B, T-1, 2, H, W) forward flow     flow_bwd: (B, T-1, 2, H, W) backward flow     weight: ...
- *Dòng:* 203

### ⚡ `flow_smoothness_loss(flow, weight)`
- *Mô tả:* Spatial smoothness of optical flow.  Args:     flow: (B, T-1, 2, H, W) optical flow     weight: scalar weight  Returns:     Weighted loss and raw loss...
- *Dòng:* 253

### ⚡ `simple_detection_loss(decoded, gt_boxes, B, T, weight)`
- *Mô tả:* Simplified detection loss using GT boxes from YOLO pseudo-labels.  Args:     decoded: List of 4 scale dicts with cx,cy,w,h (B*T, fh, fw)     gt_boxes:...
- *Dòng:* 138

### ⚡ `temporal_box_loss(decoded, B, T, weight)`
- *Mô tả:* Penalize abrupt box changes between adjacent frames.  Args:     decoded: list of 4 scale dicts, each key maps to (B*T, ...).     B, T: batch and time ...
- *Dòng:* 117

### ⚡ `video_cls_loss(video_logits, video_labels, weight)`
- *Mô tả:* Video-level cross-entropy.  Args:     video_logits: (B, nc+2) logits.     video_labels: (B,) int labels (0=SFW, 1=NSFW).     weight: scalar weight.
- *Dòng:* 101

## 📁 `FlowNSFW-main\src\flow_nsfw\model.py`
### ⚡ `**FlowNSFW**.__init__(self, dim, num_heads, num_temporal_layers, topk_global, flow_backend, temporal_backend, d_state, ssm_expand, sparse_detect, num_classes, detect_hidden)`
- *Dòng:* 54

### ⚡ `**FlowNSFW**._decode_predictions(self, raw, feat_hw, imgsz)`
- *Mô tả:* Decode raw detection heads into boxes per scale.
- *Dòng:* 170

### ⚡ `**FlowNSFW**.count_parameters(self)`
- *Dòng:* 154

### ⚡ `**FlowNSFW**.forward(self, frames, cached_flow)`
- *Mô tả:* Args:     frames: (B, T, 3, H, W) in [0,1].     cached_flow: optional pre-computed (B, T-1, 2, H, W) flow.  Returns:     dict with:       - raw: per-s...
- *Dòng:* 212

## 📁 `FlowNSFW-main\src\flow_nsfw\pseudo_labeler.py`
### ⚡ `_decode_avif_to_numpy(path)`
- *Mô tả:* Convert AVIF to RGB numpy array via ffmpeg pipe.
- *Dòng:* 30

### ⚡ `_decode_image(path)`
- *Mô tả:* Read any image as RGB numpy array.  Decode chain: cv2 → PIL/pillow-avif → ffmpeg. Returns None only if all fail.
- *Dòng:* 54

### ⚡ `build_manifest(video_roots, yolo, out_path, label, split, val_ratio, imgsz, conf, device, frame_stride, min_dir_frames)`
- *Mô tả:* Build full manifest from video directories.
- *Dòng:* 167

### ⚡ `find_frame_dirs(root, min_frames)`
- *Mô tả:* Find leaf directories containing image sequences.
- *Dòng:* 88

### ⚡ `label_video_frames(frame_dir, yolo, imgsz, conf, device, frame_stride, min_frames_for_clip)`
- *Mô tả:* Run YOLO on frames, decode AVIF→numpy as needed.  For single-frame directories (e.g. VTS sprites), repeats the frame to create a clip-able entry.
- *Dòng:* 100

### ⚡ `main()`
- *Dòng:* 218

## 📁 `FlowNSFW-main\src\flow_nsfw\ssm_backend.py`
### ⚡ `**_FallbackSSM**.__init__(self, d_model, d_state, d_conv, expand)`
- *Dòng:* 67

### ⚡ `create_ssm_layer(d_model, d_state, d_conv, expand)`
- *Mô tả:* Create the best available SSM layer.  Returns:     nn.Module with forward(x: Tensor) -> Tensor, where x is (B, L, D).
- *Dòng:* 141

### ⚡ `**_FallbackSSM**.forward(self, x)`
- *Mô tả:* x: (B, L, D)
- *Dòng:* 94

## 📁 `FlowNSFW-main\src\flow_nsfw\temporal_sparse.py`
### ⚡ `**_AttnBlock**.__init__(self, dim, num_heads)`
- *Dòng:* 38

### ⚡ `**_TransformerBlock**.__init__(self, dim, num_heads)`
- *Dòng:* 56

### ⚡ `**_MambaBlock**.__init__(self, dim, d_state, expand)`
- *Dòng:* 79

### ⚡ `**_HybridBlock**.__init__(self, dim, num_heads, d_state, expand)`
- *Dòng:* 110

### ⚡ `**SparseGlobalTemporal**.__init__(self, dim, num_heads, num_layers, topk, temporal_backend, d_state, ssm_expand)`
- *Dòng:* 161

### ⚡ `**SparseGlobalTemporal**._build_kv(self, feat, flow_fwd, t, T, q_tokens)`
- *Mô tả:* Build KV tokens: self + flow-warped neighbors + top-K global.
- *Dòng:* 204

### ⚡ `**SparseGlobalTemporal**._restore(self, x, shape)`
- *Dòng:* 200

### ⚡ `**SparseGlobalTemporal**._tokens(self, x)`
- *Dòng:* 196

### ⚡ `_topk_tokens(q, kv, k)`
- *Dòng:* 23

### ⚡ `**_AttnBlock**.forward(self, q_feat, kv_stack)`
- *Dòng:* 45

### ⚡ `**_TransformerBlock**.forward(self, q, kv)`
- *Dòng:* 67

### ⚡ `**_MambaBlock**.forward(self, x, _kv_unused)`
- *Mô tả:* x: (B, N, C). _kv_unused kept for API compatibility.
- *Dòng:* 93

### ⚡ `**_HybridBlock**.forward(self, q, kv)`
- *Dòng:* 131

### ⚡ `**SparseGlobalTemporal**.forward(self, feat, flow_fwd)`
- *Dòng:* 226

## 📁 `FlowNSFW-main\src\flow_nsfw\utils.py`
### ⚡ `resize_flow_sequence(flow, size)`
- *Mô tả:* Resize pixel-unit flow to target (H, W), rescaling magnitudes.
- *Dòng:* 25

### ⚡ `warp(feat, flow)`
- *Mô tả:* Bilinear grid_sample warp.
- *Dòng:* 8

## 📁 `LangGraph_Agent_System\projects\LocalRelay\local_relay.py`
### ⚡ `async handle_cline_request(model_name, action, request, code)`
- *Mô tả:* Endpoint hứng request HTTP từ Cline gửi qua
- *Dòng:* 42

### ⚡ `async websocket_endpoint(websocket, code, role)`
- *Mô tả:* Endpoint dành cho con App AI Studio trên trình duyệt kết nối vào
- *Dòng:* 18

## 📁 `LangGraph_Agent_System\projects\ai_trading_agent\dashboard.py`
### ⚡ `get_decisions()`
- *Dòng:* 28

### ⚡ `get_paper_trade_data()`
- *Dòng:* 17

## 📁 `LangGraph_Agent_System\projects\auto_affiliate_video\main.py`
### ⚡ `main()`
- *Dòng:* 7

## 📁 `LangGraph_Agent_System\projects\auto_x_bot\main.py`
### ⚡ `log_to_db(tweet_id, content, status)`
- *Mô tả:* Lưu lịch sử đăng Tweet vào database.
- *Dòng:* 29

### ⚡ `main()`
- *Dòng:* 59

## 📁 `LangGraph_Agent_System\projects\ceo_agent\admin_simulator.py`
### ⚡ `**AdminSimulator**.__init__(self)`
- *Dòng:* 11

### ⚡ `**AdminSimulator**._ai_handler(self)`
- *Dòng:* 59

### ⚡ `**AdminSimulator**._logic_handler(self)`
- *Dòng:* 62

### ⚡ `**AdminSimulator**.evaluate_decision(self, crisis_id, action, target)`
- *Mô tả:* Đánh giá quyết định của CEO.
- *Dòng:* 65

### ⚡ `**AdminSimulator**.get_next_crisis(self)`
- *Mô tả:* Sinh ra một cuộc khủng hoảng ngẫu nhiên.
- *Dòng:* 44

## 📁 `LangGraph_Agent_System\projects\ceo_agent\autonomous_ceo.py`
### ⚡ `**AutonomousCEO**.__init__(self)`
- *Dòng:* 69

### ⚡ `**AutonomousCEO**._build_graph(self)`
- *Dòng:* 168

### ⚡ `**AutonomousCEO**.act_node(self, state)`
- *Dòng:* 121

### ⚡ `**AutonomousCEO**.finish_node(self, state)`
- *Dòng:* 138

### ⚡ `list_projects()`
- *Mô tả:* Liệt kê tất cả các project con hiện có.
- *Dòng:* 25

### ⚡ `read_document(rel_path)`
- *Mô tả:* Đọc nội dung một file tài liệu hoặc code (truyền đường dẫn tương đối từ root).
- *Dòng:* 35

### ⚡ `**AutonomousCEO**.run_vi_hanh(self, steps)`
- *Dòng:* 185

### ⚡ `**AutonomousCEO**.should_continue(self, state)`
- *Dòng:* 163

### ⚡ `**AutonomousCEO**.think_node(self, state)`
- *Dòng:* 75

## 📁 `LangGraph_Agent_System\projects\ceo_agent\ceo_mind.py`
### ⚡ `**CEOAgent**.__init__(self)`
- *Dòng:* 29

### ⚡ `**CEOAgent**._ai_handler(self)`
- *Dòng:* 36

### ⚡ `**CEOAgent**._logic_handler(self)`
- *Dòng:* 39

### ⚡ `**CEOAgent**.handle_crisis(self, state)`
- *Mô tả:* Đưa ra quyết định dựa trên báo động hệ thống.
- *Dòng:* 42

### ⚡ `**CEOAgent**.reflect_and_learn(self, crisis_id, crisis_desc, decision, result)`
- *Mô tả:* Đúc kết bài học từ thành công hoặc thất bại.
- *Dòng:* 123

## 📁 `LangGraph_Agent_System\projects\ceo_agent\ceo_morning_routine.py`
### ⚡ `**AdminCriticAgent**._ai_handler(self, prompt_text)`
- *Dòng:* 38

### ⚡ `**CEOAgent**._ai_handler(self, prompt_text)`
- *Dòng:* 49

### ⚡ `**CEOUpgradeAgent**._ai_handler(self, prompt_text)`
- *Dòng:* 60

### ⚡ `**AdminCriticAgent**._logic_handler(self)`
- *Dòng:* 32

### ⚡ `**CEOAgent**._logic_handler(self)`
- *Dòng:* 42

### ⚡ `**CEOUpgradeAgent**._logic_handler(self)`
- *Dòng:* 54

### ⚡ `wake_up_ceo()`
- *Dòng:* 64

## 📁 `LangGraph_Agent_System\projects\ceo_agent\ceo_training_matrix.py`
### ⚡ `ceo_node(state)`
- *Dòng:* 68

### ⚡ `ceo_router(state)`
- *Dòng:* 108

### ⚡ `list_files_in_directory(directory_path)`
- *Mô tả:* Liệt kê các file trong một thư mục cụ thể để CEO có thể khám phá dự án.
- *Dòng:* 23

### ⚡ `read_ceo_lore()`
- *Mô tả:* Đọc file bộ nhớ dài hạn (Long-term Memory) của CEO để nhớ lại các bài học cũ.
- *Dòng:* 35

### ⚡ `reflect_node(state)`
- *Dòng:* 123

### ⚡ `run_nightly_training(focus_topic)`
- *Dòng:* 163

### ⚡ `summon_agent(agent_role, task_description)`
- *Mô tả:* Triệu hồi (Summon) một Agent khác (ví dụ QA_Auditor, Code_Reviewer, Trader) để nhờ phân tích/làm giúp một task. Trả về kết quả của Agent đó.
- *Dòng:* 44

## 📁 `LangGraph_Agent_System\projects\ceo_agent\marketing_intel.py`
### ⚡ `**MarketingAgent**.__init__(self)`
- *Dòng:* 16

### ⚡ `**MarketingAgent**._ai_handler(self, social_data)`
- *Dòng:* 22

### ⚡ `**MarketingAgent**._logic_handler(self, data)`
- *Dòng:* 19

### ⚡ `async main()`
- *Dòng:* 39

## 📁 `LangGraph_Agent_System\projects\gemini_cli\main.py`
### ⚡ `main()`
- *Mô tả:* Main entry point - parses arguments and runs async stream.
- *Dòng:* 69

### ⚡ `async stream_response(config, prompt, model)`
- *Mô tả:* Stream Gemini API response to stdout.  Args:     config: Configuration object.     prompt: User's prompt text.     model: Model name to use.
- *Dòng:* 22

## 📁 `LangGraph_Agent_System\projects\godot_translator\app.py`
### ⚡ `translation_worker(exe_path, target_lang, ai_model, api_key, encryption_key, lang_code)`
- *Mô tả:* Luồng dịch ngầm (Thread) để tránh block UI.
- *Dòng:* 137

## 📁 `LangGraph_Agent_System\projects\godot_translator\main_run.py`
### ⚡ `main()`
- *Mô tả:* Entry point chạy ngầm Streamlit. Dùng để thay thế file .bat cho bản Build.
- *Dòng:* 9

## 📁 `LangGraph_Agent_System\projects\godot_translator\test_translation.py`
### ⚡ `test_single_file_translation()`
- *Dòng:* 22

## 📁 `LangGraph_Agent_System\projects\jarvis-rpg-assistant\main.py`
### ⚡ `main()`
- *Dòng:* 16

## 📁 `LangGraph_Agent_System\projects\local_proxy_server\main.py`
### ⚡ `async lifespan(app)`
- *Mô tả:* Application lifespan manager.  Handles startup and shutdown events.
- *Dòng:* 30

### ⚡ `main()`
- *Mô tả:* Main entry point for the Local Proxy Server.  Starts the Uvicorn server with configuration from environment variables.
- *Dòng:* 67

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\api.py`
### ⚡ `audit_frames(request)`
- *Dòng:* 33

### ⚡ `read_root()`
- *Dòng:* 29

### ⚡ `async startup_event()`
- *Dòng:* 13

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\auditor_agent.py`
### ⚡ `**ShadowAuditorV2**.__init__(self)`
- *Dòng:* 16

### ⚡ `**ShadowAuditorV2**._ai_handler(self)`
- *Dòng:* 20

### ⚡ `**ShadowAuditorV2**._calculate_skin_percentage(self, image_path)`
- *Dòng:* 64

### ⚡ `**ShadowAuditorV2**._logic_handler(self)`
- *Dòng:* 23

### ⚡ `**ShadowAuditorV2**.analyze_frames(self, frames_dir)`
- *Dòng:* 26

### ⚡ `**ShadowAuditorV2**.generate_report(self, results)`
- *Dòng:* 75

### ⚡ `**ShadowAuditorV2**.save_json(self, results, output_path)`
- *Mô tả:* Lưu kết quả ra file JSON để làm input cho LLM.
- *Dòng:* 109

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\censorship_engine.py`
### ⚡ `**CensorshipEngine**.__init__(self)`
- *Dòng:* 13

### ⚡ `**CensorshipEngine**.censor_image(self, image_path, output_path)`
- *Mô tả:* Phát hiện và che vùng nhạy cảm trong ảnh.
- *Dòng:* 23

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\collision_logic.py`
### ⚡ `**CollisionLogic**.__init__(self)`
- *Dòng:* 11

### ⚡ `**CollisionLogic**._generate_detailed_summary(self, events)`
- *Dòng:* 50

### ⚡ `**CollisionLogic**._is_overlapping(self, box1, box2)`
- *Dòng:* 44

### ⚡ `**CollisionLogic**.detect_insertion_events(self, json_path)`
- *Dòng:* 14

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\downloader.py`
### ⚡ `download_llm()`
- *Mô tả:* Tải model TinyLlama siêu nhẹ để tóm tắt nội dung.
- *Dòng:* 9

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\identity_tracker.py`
### ⚡ `**IdentityTracker**.__init__(self, proximity_threshold)`
- *Dòng:* 12

### ⚡ `**IdentityTracker**._generate_v4_summary(self)`
- *Dòng:* 60

### ⚡ `**IdentityTracker**._update_profiles(self, frame, timestamp)`
- *Dòng:* 34

### ⚡ `**IdentityTracker**.process_timeline(self, json_data_path)`
- *Mô tả:* Đọc dữ liệu JSON và phân loại nhân vật.
- *Dòng:* 16

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\interaction_detector.py`
### ⚡ `**InteractionDetector**.__init__(self)`
- *Dòng:* 12

### ⚡ `**InteractionDetector**._calculate_distance(self, box1, box2)`
- *Dòng:* 64

### ⚡ `**InteractionDetector**._check_overlap(self, box1, box2)`
- *Dòng:* 69

### ⚡ `**InteractionDetector**._summarize_log(self, logs)`
- *Dòng:* 74

### ⚡ `**InteractionDetector**.analyze_interactions(self, json_path)`
- *Dòng:* 18

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\narrative_bridge.py`
### ⚡ `**NarrativeBridge**.__init__(self)`
- *Dòng:* 21

### ⚡ `**NarrativeBridge**._ai_handler(self, json_path, interaction_report)`
- *Mô tả:* Thử dùng AI với prompt siêu an toàn (Abstract Geometry).
- *Dòng:* 93

### ⚡ `**NarrativeBridge**._generate_rule_based_script(self, json_path, interaction_report)`
- *Mô tả:* Dùng logic quy tắc để viết kịch bản nếu AI bị chặn.
- *Dòng:* 42

### ⚡ `**NarrativeBridge**._logic_handler(self, json_path, interaction_report)`
- *Mô tả:* Fallback tối thượng: Dùng Rule Engine của chúng ta.
- *Dòng:* 102

### ⚡ `**NarrativeBridge**.run_synthesis(self, json_path, output_path)`
- *Dòng:* 106

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\processor.py`
### ⚡ `extract_keyframes(video_path, output_dir, interval_seconds)`
- *Mô tả:* Trích xuất keyframes từ video mỗi X giây.
- *Dòng:* 6

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\synthesizer.py`
### ⚡ `synthesize_narrative(json_path)`
- *Mô tả:* Đọc timeline JSON và dùng TinyLlama để viết tóm tắt diễn biến.
- *Dòng:* 11

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\video_brain.py`
### ⚡ `**VideoBrain**.__init__(self)`
- *Dòng:* 18

### ⚡ `**VideoBrain**.analyze_frame(self, image_path, question)`
- *Mô tả:* Hỏi bộ não về một frame cụ thể.
- *Dòng:* 36

### ⚡ `**VideoBrain**.describe_interaction(self, frame_paths)`
- *Mô tả:* Phân tích chuỗi hành động giữa các frame.
- *Dòng:* 49

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\vision_describer.py`
### ⚡ `**CharacterDescriber**.__init__(self)`
- *Dòng:* 23

### ⚡ `**CharacterDescriber**._ai_handler(self)`
- *Dòng:* 31

### ⚡ `**CharacterDescriber**._logic_handler(self)`
- *Dòng:* 34

### ⚡ `**CharacterDescriber**.describe_character(self, image_path)`
- *Mô tả:* Gửi ảnh 'sạch' lên Gemini để lấy mô tả ngoại hình.
- *Dòng:* 37

## 📁 `LangGraph_Agent_System\projects\nsfw_multimedia_auditor\visual_anatomy.py`
### ⚡ `**VisualAnatomyEngine**._get_dominant_color_name(self, img)`
- *Mô tả:* Xác định màu chủ đạo đơn giản.
- *Dòng:* 36

### ⚡ `**VisualAnatomyEngine**.analyze_appearance(self, image_path, detections)`
- *Mô tả:* Phân tích ngoại hình dựa trên các vùng đã phát hiện.
- *Dòng:* 13

## 📁 `LangGraph_Agent_System\projects\project_manager_sentry\governance_engine.py`
### ⚡ `**SovereignGovernance**.__init__(self)`
- *Dòng:* 6

### ⚡ `**SovereignGovernance**.check_edit_permission(self, agent_name, file_path)`
- *Mô tả:* Kiểm tra xem một Agent có quyền sửa file dựa trên OWNERS.json.
- *Dòng:* 9

### ⚡ `**SovereignGovernance**.lock_sovereign_project(self, project_name)`
- *Mô tả:* Khóa các project L3 để ngăn chặn thay đổi ngoài ý muốn.
- *Dòng:* 34

## 📁 `LangGraph_Agent_System\projects\project_manager_sentry\lifecycle_manager.py`
### ⚡ `evaluate_monorepo_health()`
- *Dòng:* 5

## 📁 `LangGraph_Agent_System\projects\project_manager_sentry\manager_agent.py`
### ⚡ `**ProjectManagerAgent**.__init__(self, name, model)`
- *Dòng:* 11

### ⚡ `**ProjectManagerAgent**.find_core_files(self, project_name)`
- *Mô tả:* Truy vấn metadata để lấy danh sách core files của một project.
- *Dòng:* 15

### ⚡ `**ProjectManagerAgent**.run(self, task)`
- *Dòng:* 37

## 📁 `LangGraph_Agent_System\projects\real_estate_prediction\app.py`
### ⚡ `home()`
- *Mô tả:* Render trang chủ với các dropdown động lấy từ data.
- *Dòng:* 46

### ⚡ `predict()`
- *Mô tả:* API endpoint xử lý dự báo giá nhà.
- *Dòng:* 160

### ⚡ `show_map()`
- *Mô tả:* Render bản đồ Heatmap giá nhà theo Quận/Huyện.
- *Dòng:* 54

## 📁 `LangGraph_Agent_System\projects\real_estate_prediction\generate_ppt_report.py`
### ⚡ `create_dashboard_ppt()`
- *Dòng:* 7

## 📁 `LangGraph_Agent_System\projects\real_estate_prediction\generate_word_report.py`
### ⚡ `create_report()`
- *Dòng:* 6

## 📁 `LangGraph_Agent_System\projects\real_estate_prediction\train_model.py`
### ⚡ `main()`
- *Dòng:* 20

## 📁 `LangGraph_Agent_System\projects\sillytavern_world_card_generator\run_nsfw_writer.py`
### ⚡ `async main()`
- *Mô tả:* Main function to run the NSFW writing workflow.
- *Dòng:* 12

## 📁 `LangGraph_Agent_System\projects\sovereign_academy\main.py`
### ⚡ `load_profile()`
- *Dòng:* 18

### ⚡ `main()`
- *Dòng:* 103

### ⚡ `run_lesson(tutor, filename, profile)`
- *Dòng:* 53

### ⚡ `save_profile(profile)`
- *Dòng:* 24

### ⚡ `update_spaced_repetition(profile, filename, score)`
- *Dòng:* 28

## 📁 `LangGraph_Agent_System\projects\sovereign_academy\one_click_learn.py`
### ⚡ `one_click_run()`
- *Dòng:* 26

## 📁 `LangGraph_Agent_System\projects\sovereign_academy\tutor_agent.py`
### ⚡ `**CodeTutorAgent**.__init__(self)`
- *Dòng:* 47

### ⚡ `**CodeTutorAgent**._ai_handler(self)`
- *Dòng:* 50

### ⚡ `**CodeTutorAgent**._logic_handler(self)`
- *Dòng:* 53

### ⚡ `**CodeTutorAgent**.explain_code(self, code, filename)`
- *Dòng:* 79

### ⚡ `**CodeTutorAgent**.generate_quiz(self, code, filename)`
- *Dòng:* 114

### ⚡ `**CodeTutorAgent**.get_random_core_file(self)`
- *Mô tả:* Lấy ngẫu nhiên 1 file Python từ core/ hoặc core_utilities/
- *Dòng:* 56

### ⚡ `**CodeTutorAgent**.read_code(self, file_path)`
- *Dòng:* 70

## 📁 `LangGraph_Agent_System\projects\sovereign_terminal\airdrop_mcp_farmer.py`
### ⚡ `async farm_faucet(target_url, wallet_address)`
- *Mô tả:* Sử dụng Playwright MCP (qua mcp_client.py) để tự động hóa trình duyệt thay vì dùng thư viện playwright trực tiếp. Điều này giúp Terminal Headless có t...
- *Dòng:* 26

### ⚡ `async send_telegram_alert(message)`
- *Dòng:* 14

## 📁 `LangGraph_Agent_System\projects\sovereign_terminal\daemon.py`
### ⚡ `main()`
- *Dòng:* 83

### ⚡ `async run_forever()`
- *Mô tả:* Chạy vòng lặp vô tận (Daemon) - Level 4 Event-Driven.
- *Dòng:* 50

### ⚡ `async send_telegram_message(message)`
- *Mô tả:* Gửi tin nhắn qua Telegram dùng TELE_TOKEN và CHAT_ID.
- *Dòng:* 17

### ⚡ `async task_morning_briefing()`
- *Mô tả:* Chạy báo cáo buổi sáng.
- *Dòng:* 35

## 📁 `LangGraph_Agent_System\projects\sovereign_terminal\main.py`
### ⚡ `async async_main()`
- *Mô tả:* Entry point.
- *Dòng:* 163

### ⚡ `async chat_loop(client, model, system_prompt)`
- *Mô tả:* Vòng lặp Chat REPL (Read-Eval-Print Loop).
- *Dòng:* 90

### ⚡ `async handle_tool_calls(client, model, messages, tool_calls)`
- *Mô tả:* Xử lý tool calls từ AI, trả về kết quả cho AI. Hỗ trợ nhiều tool calls liên tiếp.
- *Dòng:* 49

### ⚡ `main()`
- *Dòng:* 194

### ⚡ `print_banner()`
- *Mô tả:* In banner khi khởi động.
- *Dòng:* 35

## 📁 `LangGraph_Agent_System\projects\trading_rpg_simulator\dungeon_master.py`
### ⚡ `**DungeonMaster**.__init__(self)`
- *Dòng:* 13

### ⚡ `**DungeonMaster**.generate_next_turn(self)`
- *Mô tả:* Sinh ra dữ liệu cho 1 lượt chơi (1 ngày).
- *Dòng:* 26

### ⚡ `**DungeonMaster**.resolve_combat(self, action, price_impact, current_capital)`
- *Mô tả:* Tính toán PnL dựa trên quyết định của TraderHero và biến động thực tế.
- *Dòng:* 40

## 📁 `LangGraph_Agent_System\projects\trading_rpg_simulator\trader_hero.py`
### ⚡ `**TraderHero**.__init__(self)`
- *Dòng:* 29

### ⚡ `**TraderHero**.make_decision(self, state, current_capital)`
- *Mô tả:* Đưa ra quyết định dựa trên tin tức hiện tại và ký ức.
- *Dòng:* 36

### ⚡ `**TraderHero**.reflect_and_learn(self, combat_result, news)`
- *Mô tả:* Đúc kết kinh nghiệm sau mỗi trận đấu (ngày).
- *Dòng:* 87

## 📁 `LangGraph_Agent_System\projects\universal_web_scraper\main.py`
### ⚡ `download_html(url)`
- *Mô tả:* Tải toàn bộ mã nguồn HTML từ một URL và lưu vào file cục bộ.  Args:     url (str): Đường dẫn trang web cần cào dữ liệu.      Returns:     bool: True n...
- *Dòng:* 20

### ⚡ `main()`
- *Dòng:* 50

## 📁 `LangGraph_Agent_System\src\factory\config.py`
### ⚡ `create_fallback_chain(model_list, temperature, max_tokens)`
- *Mô tả:* Creates a chain of LLMs with fallbacks. Bọc thêm Retry để chống Rate Limit 429/403.
- *Dòng:* 67

### ⚡ `**Config**.get_llm_credentials()`
- *Mô tả:* Returns a list of available API credentials, prioritized for survival.
- *Dòng:* 28

### ⚡ `**Config**.initialize(cls)`
- *Dòng:* 23

## 📁 `LangGraph_Agent_System\src\factory\main.py`
### ⚡ `build_meta_graph()`
- *Mô tả:* Builds the main "meta-graph" that orchestrates all other workflows. Bao gồm tích hợp luồng Codebase Audit Pipeline.
- *Dòng:* 107

### ⚡ `debate_graph(state)`
- *Dòng:* 38

### ⚡ `async main(mode, project_name, user_requirement, file_path)`
- *Dòng:* 221

### ⚡ `overlord_graph(state)`
- *Dòng:* 30

### ⚡ `post_prd_update(state)`
- *Mô tả:* Update state after PRD generation. This function will be a node that follows product_ba_node.
- *Dòng:* 80

### ⚡ `primary_router(state)`
- *Mô tả:* Lớp bảo vệ đầu tiên: Phân luồng ngay từ đầu để tránh nhét rác vào Overlord.
- *Dòng:* 43

### ⚡ `product_ba_node(state)`
- *Dòng:* 26

### ⚡ `production_graph(state)`
- *Dòng:* 34

### ⚡ `project_manager_node(state)`
- *Dòng:* 96

### ⚡ `route_to_workflow(state)`
- *Mô tả:* Routes to the appropriate sub-workflow based on the Overlord's decision.
- *Dòng:* 61

## 📁 `LangGraph_Agent_System\src\scrapers\auto_repair_selector.py`
### ⚡ `**AutoRepairSelector**.__init__(self)`
- *Dòng:* 28

### ⚡ `**AutoRepairSelector**._ai_handler(self)`
- *Dòng:* 35

### ⚡ `**AutoRepairSelector**._logic_handler(self)`
- *Dòng:* 31

### ⚡ `**AutoRepairSelector**.repair_and_patch(self, file_path, failed_selector, html_snippet, target_desc, http_status)`
- *Mô tả:* Thực hiện quy trình sửa lỗi và vá code tự động. Tích hợp [Anti-Bot Guard]: Kháng độc Cloudflare & Blocked IP.
- *Dòng:* 56

## 📁 `LangGraph_Agent_System\src\skills\search_knowledge_base.py`
### ⚡ `search_research_papers(query)`
- *Mô tả:* Tìm kiếm kiến thức chuyên sâu từ Tàng Kinh Các (Knowledge Database). Sử dụng Tool này khi cần tìm hiểu về các chiến lược Marketing, thuật toán AI (ReA...
- *Dòng:* 21

## 📁 `LangGraph_Agent_System\src\skills\skill_manager.py`
### ⚡ `**SkillManager**.__init__(self)`
- *Mô tả:* Khởi tạo Skill Manager.
- *Dòng:* 13

### ⚡ `**SkillManager**.load_skill(self, skill_name)`
- *Mô tả:* Tải một kỹ năng cụ thể.  Args:     skill_name (str): Tên kỹ năng cần tải.
- *Dòng:* 17

## 📁 `Project\LangGraph_Agent_System\core\drm_validator.py`
### ⚡ `check_license_validity()`
- *Mô tả:* Core DRM Logic. This file should be compiled to .pyd / .so using Cython to prevent reverse engineering.
- *Dòng:* 7

### ⚡ `init_drm()`
- *Dòng:* 46

## 📁 `Project\LangGraph_Agent_System\core\logic_auditor.py`
### ⚡ `**LogicAuditor**.__init__(self)`
- *Dòng:* 11

### ⚡ `**LogicAuditor**.evaluate_evolution(self, task_name, current_metrics)`
- *Mô tả:* Đánh giá bản nháp so với tiêu chuẩn hệ thống.  Tiêu chuẩn chấp nhận (LV4): - Latency < 60s (cho sub-task). - RAM tăng thêm < 200MB. - Tỷ lệ lỗi = 0.
- *Dòng:* 20

### ⚡ `**LogicAuditor**.start_session(self)`
- *Mô tả:* Bắt đầu đo lường tài nguyên trước khi Agent thực thi nháp.
- *Dòng:* 15

## 📁 `Project\LangGraph_Agent_System\core\mental_sandbox.py`
### ⚡ `**MentalSandbox**.__init__(self, root_dir)`
- *Dòng:* 20

### ⚡ `**MentalSandbox**._ensure_sandbox(self)`
- *Dòng:* 25

### ⚡ `**MentalSandbox**.cleanup(self)`
- *Mô tả:* Dọn dẹp sandbox.
- *Dòng:* 121

### ⚡ `**MentalSandbox**.create_draft(self, original_file, new_content)`
- *Mô tả:* Tạo bản nháp của file trong sandbox.
- *Dòng:* 29

### ⚡ `**MentalSandbox**.deploy_draft(self, draft_path, original_file)`
- *Mô tả:* Merge bản nháp vào file gốc sau khi đã qua kiểm duyệt.
- *Dòng:* 115

### ⚡ `**MentalSandbox**.run_unit_tests(self, test_pattern)`
- *Mô tả:* Chạy các bài unit test liên quan.
- *Dòng:* 89

### ⚡ `**MentalSandbox**.verify_logic(self, tree)`
- *Mô tả:* [VULN-001] Kiểm tra các lỗi logic nguy hiểm (Runtime Risks).
- *Dòng:* 60

### ⚡ `**MentalSandbox**.verify_syntax(self, file_path)`
- *Mô tả:* Kiểm tra lỗi cú pháp (Syntax Check) bằng AST.
- *Dòng:* 42

## 📁 `Project\LangGraph_Agent_System\core\post_mortem_engine.py`
### ⚡ `**PostMortemEngine**.__init__(self, db_path)`
- *Dòng:* 12

### ⚡ `**PostMortemEngine**._log_failure(self, reason)`
- *Mô tả:* Cập nhật vào FAILED_PATHS.json
- *Dòng:* 40

### ⚡ `**PostMortemEngine**.analyze_recent_trades(self, limit)`
- *Mô tả:* Phân tích các lệnh giao dịch gần đây.
- *Dòng:* 17

## 📁 `Project\LangGraph_Agent_System\core\principles_enforcer.py`
### ⚡ `**PrinciplesEnforcer**.__init__(self)`
- *Dòng:* 9

### ⚡ `**PrinciplesEnforcer**.audit_agent_output(self, output)`
- *Mô tả:* Chấm điểm độ tuân thủ nguyên lý của văn bản (0.0 - 1.0)
- *Dòng:* 34

### ⚡ `**PrinciplesEnforcer**.verify_decision(self, agent_role, decision)`
- *Mô tả:* Kiểm tra xem quyết định có vi phạm nguyên lý cốt lõi không.
- *Dòng:* 18

## 📁 `Project\LangGraph_Agent_System\core\process_watchdog.py`
### ⚡ `**ProcessWatchdog**.__init__(self, max_ram_mb, max_timeout_s)`
- *Dòng:* 17

### ⚡ `**ProcessWatchdog**.log_failure(self, reason)`
- *Mô tả:* Ghi tội danh của tiến trình bị trảm vào FAILED_PATHS.json.
- *Dòng:* 24

### ⚡ `**ProcessWatchdog**.monitor_pid(self, pid)`
- *Mô tả:* Giám sát một tiến trình và TOÀN BỘ tiến trình con của nó. Trả về True nếu an toàn, False nếu có tiến trình bị KILL.
- *Dòng:* 43

## 📁 `Project\LangGraph_Agent_System\core_utilities\backup_manager.py`
### ⚡ `backup_databases()`
- *Mô tả:* Nén tất cả các file .db (SQLite) thành file zip để backup.
- *Dòng:* 37

### ⚡ `backup_full_workspace()`
- *Mô tả:* Nén Zip toàn bộ thư mục workspace ngoại trừ các thư mục ảo/không cần thiết.
- *Dòng:* 92

### ⚡ `backup_loop()`
- *Mô tả:* Chạy vòng lặp ngầm (cronjob) backup định kỳ mỗi 24 tiếng.
- *Dòng:* 142

### ⚡ `clean_old_backups(backup_dir, prefix, keep_last)`
- *Mô tả:* Giữ lại `keep_last` file backup mới nhất và xóa các file cũ hơn.
- *Dòng:* 131

### ⚡ `get_storage_dir()`
- *Mô tả:* Lấy thư mục data lưu trữ hiện tại (ưu tiên ổ D nếu có trong biến môi trường)
- *Dòng:* 28

## 📁 `Project\LangGraph_Agent_System\core_utilities\http_client.py`
### ⚡ `**HTTPClient**.get(url, params, headers, timeout, use_httpx)`
- *Dòng:* 11

### ⚡ `**HTTPClient**.post(url, data, json, headers, timeout, use_httpx)`
- *Dòng:* 23

## 📁 `Project\LangGraph_Agent_System\core_utilities\image_utils.py`
### ⚡ `encode_image(image_path)`
- *Mô tả:* Chuyển đổi hình ảnh sang định dạng Base64.  Args:     image_path (str): Đường dẫn tuyệt đối hoặc tương đối tới file ảnh.      Returns:     str: Chuỗi ...
- *Dòng:* 4

## 📁 `Project\LangGraph_Agent_System\core_utilities\logger.py`
### ⚡ `**TelegramAlertHandler**.__init__(self)`
- *Dòng:* 14

### ⚡ `**TelegramAlertHandler**._send_message(self, payload)`
- *Dòng:* 38

### ⚡ `**TelegramAlertHandler**.emit(self, record)`
- *Dòng:* 20

### ⚡ `get_logger(name)`
- *Mô tả:* Tạo và trả về một logger tập trung cho dự án. Hỗ trợ Rotate Log để không làm đầy ổ cứng.
- *Dòng:* 47

## 📁 `Project\LangGraph_Agent_System\core_utilities\notification_gateway.py`
### ⚡ `send_alert(message, level, component)`
- *Mô tả:* Gửi cảnh báo qua Telegram
- *Dòng:* 9

## 📁 `Project\LangGraph_Agent_System\core_utilities\obfuscator.py`
### ⚡ `**CodeObfuscator**.__init__(self)`
- *Dòng:* 12

### ⚡ `**CodeObfuscator**._generate_random_name(self, length)`
- *Mô tả:* Tao ten bien/ham ngau nhien.
- *Dòng:* 17

### ⚡ `**CodeObfuscator**.obfuscate_file(self, input_path)`
- *Mô tả:* Xao tron mot file Python co ban.
- *Dòng:* 21

## 📁 `Project\LangGraph_Agent_System\core_utilities\process_watchdog.py`
### ⚡ `check_and_kill_zombies()`
- *Dòng:* 78

### ⚡ `check_system_health()`
- *Mô tả:* Kiểm tra tổng thể CPU và RAM hệ thống để cảnh báo (Task 2.3)
- *Dòng:* 55

### ⚡ `is_zombie_browser(proc)`
- *Mô tả:* Kiểm tra xem đây có phải là Zombie Process Browser từ Playwright/Selenium không
- *Dòng:* 37

### ⚡ `watchdog_loop()`
- *Dòng:* 124

## 📁 `Project\LangGraph_Agent_System\core_utilities\safe_file_manager.py`
### ⚡ `**SafeFileManager**.__init__(self)`
- *Dòng:* 12

### ⚡ `**SafeFileManager**.request_merge(self, draft_path, target_path, task_name)`
- *Mô tả:* Gửi yêu cầu merge từ Sandbox vào file gốc. Chỉ thực hiện nếu LogicAuditor xác nhận 'Evolution Confirmed'.
- *Dòng:* 29

### ⚡ `**SafeFileManager**.write_to_sandbox(self, file_path, content)`
- *Mô tả:* Viết code nháp vào Sandbox để kiểm thử.
- *Dòng:* 17

## 📁 `Project\LangGraph_Agent_System\core_utilities\self_healing.py`
### ⚡ `**SelfHealingWatchdog**.__init__(self)`
- *Dòng:* 36

### ⚡ `**SelfHealingWatchdog**.check_proxy_alive(self)`
- *Mô tả:* Kiem tra xem Local Proxy co dang phan hoi khong.
- *Dòng:* 41

### ⚡ `**SelfHealingWatchdog**.monitor_loop(self)`
- *Dòng:* 84

### ⚡ `**SelfHealingWatchdog**.repair_python_path(self, env_dict)`
- *Mô tả:* [V2] Tu dong thiet lap PYTHONPATH chuan de fix loi ModuleNotFoundError.
- *Dòng:* 50

### ⚡ `**SelfHealingWatchdog**.restart_proxy(self)`
- *Mô tả:* Khoi dong lai Local Proxy Server voi co che tu sua duong dan.
- *Dòng:* 59

## 📁 `Project\LangGraph_Agent_System\src\api_gateway.py`
### ⚡ `**CentralizedAPIGateway**.__init__(self, db_path, failure_threshold, recovery_timeout)`
- *Dòng:* 17

### ⚡ `**CentralizedAPIGateway**._get_state(self)`
- *Mô tả:* Retrieves the current state of the circuit breaker from the database.
- *Dòng:* 49

### ⚡ `**CentralizedAPIGateway**._initialize_db(self)`
- *Mô tả:* Initializes the SQLite database for circuit breaker state and LLM caching.
- *Dòng:* 23

### ⚡ `**CentralizedAPIGateway**._record_failure(self)`
- *Mô tả:* Records a failure and updates the failure count.
- *Dòng:* 75

### ⚡ `**CentralizedAPIGateway**._record_success(self)`
- *Mô tả:* Records a success and resets the failure count if in HALF_OPEN state.
- *Dòng:* 87

### ⚡ `**CentralizedAPIGateway**._set_state(self, state, failure_count, last_failure_time)`
- *Mô tả:* Updates the state of the circuit breaker in the database.
- *Dòng:* 58

### ⚡ `**CentralizedAPIGateway**.circuit_breaker(self, service_name)`
- *Mô tả:* Decorator for applying circuit breaker logic to a function.
- *Dòng:* 134

### ⚡ `**CentralizedAPIGateway**.get_cached_response(self, prompt, schema_str)`
- *Mô tả:* Lấy phản hồi từ cache SQLite.
- *Dòng:* 97

### ⚡ `**CentralizedAPIGateway**.save_to_cache(self, prompt, response, schema_str)`
- *Mô tả:* Lưu phản hồi vào cache SQLite.
- *Dòng:* 121

## 📁 `Project\LangGraph_Agent_System\src\base_agent.py`
### ⚡ `**BaseAgent**.__init__(self, name, role, model_name, temperature, agent_label)`
- *Dòng:* 51

### ⚡ `**BaseAgent**._ai_handler(self)`
- *Dòng:* 282

### ⚡ `**BaseAgent**._call_llm(self, prompt, is_json, schema, tools, use_jit_context)`
- *Mô tả:* Wrapper an toàn bọc Try-Except ngoài cùng cho hệ thống
- *Dòng:* 250

### ⚡ `**BaseAgent**._call_llm_with_retry(self, prompt, is_json, schema, tools, use_jit_context)`
- *Mô tả:* Luồng gọi LLM khép kín với đầy đủ cơ chế Retry và dán nhãn Agent. Tích hợp [Self-Healing Memory] tự động nạp ký ức thất bại và Tool Empowerment.
- *Dòng:* 82

### ⚡ `**BaseAgent**._extract_json_from_text(self, text)`
- *Mô tả:* Tách JSON ra khỏi Markdown Code blocks an toàn.
- *Dòng:* 228

### ⚡ `**BaseAgent**._logic_handler(self)`
- *Dòng:* 286

### ⚡ `**BaseAgent**._parse_json_response(self, response_text, schema)`
- *Dòng:* 267

### ⚡ `**BaseAgent**.execute(self)`
- *Mô tả:* Mô hình Cầu Dao Điện (Circuit Breaker Pattern) + Watchdog Guardian.
- *Dòng:* 289

## 📁 `Project\LangGraph_Agent_System\src\database.py`
### ⚡ `**SystemDB**.__init__(self)`
- *Dòng:* 22

### ⚡ `**SystemDB**._create_tables(self)`
- *Dòng:* 32

### ⚡ `**SystemDB**.close(self)`
- *Dòng:* 156

### ⚡ `**SystemDB**.get_latest_backtests(self, limit)`
- *Dòng:* 133

### ⚡ `**SystemDB**.get_latest_decisions(self, limit)`
- *Dòng:* 128

### ⚡ `**SystemDB**.get_latest_paper_trade_balance(self)`
- *Dòng:* 148

### ⚡ `**SystemDB**.get_latest_updates(self, limit)`
- *Dòng:* 138

### ⚡ `**SystemDB**.get_paper_trade_history(self, limit)`
- *Dòng:* 143

### ⚡ `**SystemDB**.log_backtest_report(self, ticker, start_date, end_date, initial, final, roi, sharpe, max_dd, win_rate)`
- *Dòng:* 101

### ⚡ `**SystemDB**.log_paper_trade_balance(self, btc_bal, eth_bal, sol_bal, usdt_bal, total_val)`
- *Dòng:* 119

### ⚡ `**SystemDB**.log_project_update(self, module, description)`
- *Dòng:* 110

### ⚡ `**SystemDB**.log_trading_decision(self, ticker, price, action, confidence, sl, tp, reasoning)`
- *Dòng:* 92

## 📁 `Project\LangGraph_Agent_System\src\resume_flow.py`
### ⚡ `get_latest_checkpoint(db_path)`
- *Mô tả:* Lấy Checkpoint state mới nhất từ SQLite
- *Dòng:* 20

### ⚡ `main()`
- *Dòng:* 76

### ⚡ `async resume_graph(state)`
- *Dòng:* 50

## 📁 `Project\LangGraph_Agent_System\src\token_tracker.py`
### ⚡ `**TokenTracker**.__init__(self)`
- *Dòng:* 10

### ⚡ `**TokenTracker**._calculate_cost(self, model_name, prompt_tokens, completion_tokens)`
- *Mô tả:* Tính toán chi phí dựa trên bảng giá (tham khảo). Giá có thể thay đổi, đây là mức giá ước tính (USD / 1M tokens).
- *Dòng:* 35

### ⚡ `**TokenTracker**._init_db(self)`
- *Dòng:* 17

### ⚡ `**TokenTracker**.get_total_cost(self, project_name)`
- *Dòng:* 78

### ⚡ `**TokenTracker**.log_usage(self, project_name, model_name, prompt_tokens, completion_tokens)`
- *Dòng:* 55

### ⚡ `track_llm_usage(response, project_name, model_name)`
- *Mô tả:* Helper function để parse token usage từ response của LangChain/OpenAI và log vào database.
- *Dòng:* 93

## 📁 `airdrop_guerrilla\src\analysis\scoring.py`
### ⚡ `**AirdropScoringEngine**.__init__(self, db_path)`
- *Dòng:* 111

### ⚡ `**AlphaAnalyzer**.analyze_projects(cls, projects)`
- *Mô tả:* Phân tích và chấm điểm hàng loạt dự án.  Args:     projects (List[Dict]): Danh sách thông tin dự án.      Returns:     List[Dict]: Danh sách dự án đã ...
- *Dòng:* 83

### ⚡ `**AlphaAnalyzer**.calculate_score(cls, funding_amount, investors, risk_factor)`
- *Mô tả:* Tính toán điểm số tiềm năng (Alpha Score). Công thức: Score = (Funding_Amount * VC_Tier_Weight) / Risk_Factor  Args:     funding_amount (float): Tổng ...
- *Dòng:* 61

### ⚡ `**AirdropScoringEngine**.calculate_wallet_metrics(self, wallet_address)`
- *Mô tả:* Truy vấn SQLite và tính toán ma trận điểm cho từng ví.
- *Dòng:* 118

### ⚡ `**AirdropScoringEngine**.generate_markdown_report(self, output_path)`
- *Mô tả:* Quét toàn bộ ví trong DB và tạo báo cáo Markdown.
- *Dòng:* 159

### ⚡ `**AlphaAnalyzer**.get_vc_weight(cls, investors)`
- *Mô tả:* Xác định trọng số lớn nhất dựa trên danh sách các quỹ đầu tư của dự án. Chỉ cần có 1 quỹ Tier 1 tham gia là dự án được tính điểm Tier 1.  Args:     in...
- *Dòng:* 32

## 📁 `airdrop_guerrilla\src\automation\executor.py`
### ⚡ `**AirdropExecutor**.__init__(self, action_plan_path, wallet_manager, notifier)`
- *Dòng:* 32

### ⚡ `**AirdropExecutor**._ai_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 43

### ⚡ `**AirdropExecutor**._discord_join(self, page, context, invite_url, wallet_address)`
- *Mô tả:* Logic tự động Join Discord.
- *Dòng:* 272

### ⚡ `**AirdropExecutor**._handle_faucet_demo(self, page, url, address)`
- *Mô tả:* Logic mẫu cho việc qua mặt Faucet (Dán ví -> Giải Captcha -> Click). Sử dụng 2Captcha để vượt qua iframe xác thực.
- *Dòng:* 164

### ⚡ `**AirdropExecutor**._logic_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 47

### ⚡ `**AirdropExecutor**._twitter_interact(self, page, context, action, url, wallet_address)`
- *Mô tả:* Logic tương tác tự động với Twitter (X) kèm Natural Browsing.
- *Dòng:* 248

### ⚡ `**AirdropExecutor**._verify_login_status(self, page, context, platform, wallet_address)`
- *Mô tả:* Kiểm tra xem trang hiện tại đã được đăng nhập hay chưa (chờ tối đa 15s).
- *Dòng:* 223

### ⚡ `**AirdropExecutor**.execute_wallet(self, wallet_address)`
- *Mô tả:* Khởi chạy kịch bản farm cho một ví cụ thể.
- *Dòng:* 51

## 📁 `airdrop_guerrilla\src\automation\multi_account.py`
### ⚡ `**MultiAccountManager**.__init__(self, base_profile_dir)`
- *Dòng:* 10

### ⚡ `**MultiAccountManager**.delete_account(self, account_id)`
- *Mô tả:* Xoa mot account va du lieu profile di kem.
- *Dòng:* 29

### ⚡ `**MultiAccountManager**.get_account_profile_path(self, account_id)`
- *Mô tả:* Lay duong dan thu muc profile cho mot account cu the.
- *Dòng:* 19

### ⚡ `**MultiAccountManager**.list_accounts(self)`
- *Mô tả:* Liet ke danh sach cac account hien co.
- *Dòng:* 25

## 📁 `airdrop_guerrilla\src\automation\session_manager.py`
### ⚡ `**SessionManager**.apply_discord_session(context, token)`
- *Mô tả:* Nạp Token của Discord vào Local Storage thông qua add_init_script.  Args:     context: Playwright Browser Context.     token (str): Token đăng nhập củ...
- *Dòng:* 62

### ⚡ `**SessionManager**.apply_twitter_session(context, auth_data)`
- *Mô tả:* Nạp auth_token của X (Twitter) hoặc một mảng JSON Cookie vào Browser Context.  Args:     context: Playwright Browser Context.     auth_data (str): Giá...
- *Dòng:* 7

## 📁 `airdrop_guerrilla\src\automation\stealth_behavior.py`
### ⚡ `**StealthBrowser**.__init__(self, headless)`
- *Dòng:* 12

### ⚡ `async **StealthBrowser**.human_click(self, page, selector)`
- *Mô tả:* Giả lập thao tác click chuột của người dùng (có di chuyển).
- *Dòng:* 86

### ⚡ `async **StealthBrowser**.human_scroll(self, page, scrolls)`
- *Mô tả:* Giả lập thao tác cuộn trang của người dùng.
- *Dòng:* 78

### ⚡ `async **StealthBrowser**.init_browser(self, playwright, profile_dir)`
- *Mô tả:* Khởi tạo Persistent Browser Context để lưu Cookies và Extension.
- *Dòng:* 15

### ⚡ `async **StealthBrowser**.random_delay(self, min_ms, max_ms)`
- *Mô tả:* Tạo độ trễ ngẫu nhiên giống con người.
- *Dòng:* 73

### ⚡ `async **StealthBrowser**.stealth_page(self, page)`
- *Mô tả:* Bơm stealth xịn vào page và giả lập vân tay trình duyệt (Canvas, WebGL).
- *Dòng:* 51

## 📁 `airdrop_guerrilla\src\automation\wallet_manager.py`
### ⚡ `**WalletManager**.__init__(self, db_path, master_key)`
- *Dòng:* 13

### ⚡ `**WalletManager**._load_db(self)`
- *Mô tả:* Tải dữ liệu ví từ file JSON.
- *Dòng:* 50

### ⚡ `**WalletManager**._save_db(self)`
- *Mô tả:* Lưu trữ dữ liệu ví xuống file JSON.
- *Dòng:* 57

### ⚡ `**WalletManager**.add_wallet(self, address, private_key, name, twitter_token, discord_token, proxy_url)`
- *Mô tả:* Thêm một ví mới, mã hóa Private Key, X auth_token, Discord token và gán User-Agent tĩnh. Hỗ trợ gắn thêm Proxy để Route IP riêng lẻ.
- *Dòng:* 86

### ⚡ `**WalletManager**.generate_static_user_agent(self, address)`
- *Mô tả:* Sinh ra một User-Agent CỐ ĐỊNH dựa trên địa chỉ ví (Chống Sybil).
- *Dòng:* 62

### ⚡ `**WalletManager**.get_decrypted_data(self, address)`
- *Mô tả:* Lấy và giải mã Private Key và các Token mxh.
- *Dòng:* 113

## 📁 `airdrop_guerrilla\src\automation\zealy_bot.py`
### ⚡ `**ZealyBot**.__init__(self, community_slug)`
- *Dòng:* 20

### ⚡ `async **ZealyBot**.run_quests(self)`
- *Mô tả:* Khởi động luồng chạy quest tự động
- *Dòng:* 24

## 📁 `airdrop_guerrilla\src\modes\full_auto_cli.py`
### ⚡ `execute_random_action(chain_instance, wallet_address, network_name)`
- *Mô tả:* Áp dụng thuật toán xúc xắc 80/20 chống bộ lọc Sybil (Với Jitter Amount).
- *Dòng:* 82

### ⚡ `log_transaction_to_db(wallet_address, network, action, tx_hash, status, error_msg)`
- *Mô tả:* Ghi nhận lịch sử giao dịch vào SQLite Database để phục vụ chấm điểm sau này.
- *Dòng:* 53

### ⚡ `main()`
- *Dòng:* 132

### ⚡ `send_telegram_message(message)`
- *Mô tả:* Gửi thông báo qua Telegram
- *Dòng:* 36

## 📁 `airdrop_guerrilla\src\modes\semi_auto_ui.py`
### ⚡ `alert_user_for_manual_action(message)`
- *Mô tả:* Kích hoạt chuông báo (Beep) và dừng chương trình chờ người dùng can thiệp. (Ví dụ: Giải Captcha Cloudflare hoặc Confirm Wallet).
- *Dòng:* 17

### ⚡ `run_semi_auto_quests()`
- *Dòng:* 34

## 📁 `airdrop_guerrilla\src\networks\evm_base.py`
### ⚡ `**EVMBase**.__init__(self, network_name, rpc_urls, chain_id, private_key, symbol, explorer_url, proxy_url)`
- *Dòng:* 26

### ⚡ `**EVMBase**.check_balance_and_survival(self)`
- *Mô tả:* Kiểm tra số dư tối thiểu, bắn Telegram báo động nếu cạn tiền.
- *Dòng:* 86

### ⚡ `**EVMBase**.deploy_dummy_contract(self)`
- *Mô tả:* Triển khai một Smart Contract rỗng (Dummy Contract). Bí quyết Airdrop: Các ví có lịch sử Deploy Contract thường được đánh giá là "Dev Wallet".
- *Dòng:* 149

### ⚡ `**EVMBase**.fragment_amount(self, total_amount, parts)`
- *Mô tả:* Chia nho so luong token thanh cac phan ngau nhien de lam nhiễu analysis.
- *Dòng:* 200

### ⚡ `**EVMBase**.get_balance(self)`
- *Mô tả:* Lấy số dư Native Token của ví.
- *Dòng:* 63

### ⚡ `**EVMBase**.get_gas_price(self, wait_for_low_gas, max_gwei)`
- *Mô tả:* Lấy giá Gas hiện tại. Hỗ trợ Gas-Optimization: Chờ đợi gas thấp.
- *Dòng:* 68

### ⚡ `**EVMBase**.init_fallback_connection(self)`
- *Mô tả:* Duyệt danh sách RPC, tự động chuyển mạch nếu có node sập.
- *Dòng:* 43

### ⚡ `**EVMBase**.random_delay(self, min_sec, max_sec)`
- *Mô tả:* [UPGRADE] Gaussian Random Delay de lach bo loc Sybil. Su dung phan phoi chuan (Gaussian) de tao do tre tu nhien hon.
- *Dòng:* 188

### ⚡ `**EVMBase**.send_native_token(self, to_address, amount_ether)`
- *Mô tả:* Gửi Native Token (Ví dụ: ETH -> Soneium, MON -> Monad) Mục đích: Cày Transaction Hash (TX) để làm mượt ví. Đã bọc Tenacity Retry để tự gửi lại nếu ngh...
- *Dòng:* 106

## 📁 `airdrop_guerrilla\src\networks\inco.py`
### ⚡ `**IncoNetwork**.__init__(self, private_key, proxy_url)`
- *Dòng:* 5

## 📁 `airdrop_guerrilla\src\networks\monad.py`
### ⚡ `**MonadNetwork**.__init__(self, private_key, proxy_url)`
- *Dòng:* 5

## 📁 `airdrop_guerrilla\src\networks\soneium.py`
### ⚡ `**SoneiumNetwork**.__init__(self, private_key, proxy_url)`
- *Dòng:* 5

## 📁 `airdrop_guerrilla\src\scrapers\defillama_funding_parser.py`
### ⚡ `**DefiLlamaParser**.__init__(self, log_file)`
- *Dòng:* 19

### ⚡ `**DefiLlamaParser**.fetch_live_raises(self)`
- *Mô tả:* Gọi API thực tế từ DefiLlama và xử lý dữ liệu trả về.  Returns:     List[Dict]: Danh sách 100 dự án gọi vốn mới nhất đã chuẩn hóa cấu trúc.
- *Dòng:* 23

### ⚡ `**DefiLlamaParser**.run_live_pipeline(self, output_csv)`
- *Mô tả:* Khởi chạy chu trình Cào -> Phân tích -> Lưu trữ cho Phase 2.
- *Dòng:* 86

## 📁 `airdrop_guerrilla\src\utils\base_scraper.py`
### ⚡ `**BaseScraper**.__init__(self, log_file)`
- *Mô tả:* Khởi tạo BaseScraper.  Args:     log_file (str): Đường dẫn đến file lưu trữ danh sách các trang/URL đã cào thành công.
- *Dòng:* 15

### ⚡ `**BaseScraper**.add_scraped_item(self, item_id)`
- *Mô tả:* Ghi nhận một item (trang/URL/ID) đã cào thành công vào file log.  Args:     item_id (str): ID, số trang, hoặc URL định danh.
- *Dòng:* 40

### ⚡ `**BaseScraper**.build_headers(self)`
- *Mô tả:* Tạo HTTP Headers ngẫu nhiên với IP spoofing và User-Agent mới để vượt qua WAF (Web Application Firewall).  Returns:     Dict[str, str]: Dictionary chứ...
- *Dòng:* 50

### ⚡ `**BaseScraper**.fetch_url(self, url)`
- *Mô tả:* Thực hiện HTTP GET Request một cách an toàn (State-less) với Exponential Backoff. Retry tối đa 3 lần nếu gặp lỗi 429 hoặc 5xx.  Args:     url (str): U...
- *Dòng:* 85

### ⚡ `**BaseScraper**.get_scraped_items(self)`
- *Mô tả:* Đọc danh sách các items (trang/URL/ID) đã cào thành công từ log file.  Returns:     Set[str]: Tập hợp các ID hoặc số trang đã được cào.
- *Dòng:* 27

### ⚡ `**BaseScraper**.sleep_random(self, min_seconds, max_seconds)`
- *Mô tả:* Tạm dừng thực thi một khoảng thời gian ngẫu nhiên để giả lập thao tác của con người.  Args:     min_seconds (float): Thời gian chờ tối thiểu.     max_...
- *Dòng:* 74

## 📁 `airdrop_guerrilla\src\utils\migrate_to_sqlite.py`
### ⚡ `init_db()`
- *Dòng:* 10

### ⚡ `migrate_data(conn)`
- *Dòng:* 44

## 📁 `airdrop_guerrilla\src\utils\notifier.py`
### ⚡ `**TelegramNotifier**.__init__(self)`
- *Dòng:* 13

### ⚡ `**TelegramNotifier**.is_configured(self)`
- *Mô tả:* Kiểm tra xem đã cấu hình đủ Token và Chat ID chưa.
- *Dòng:* 18

### ⚡ `**TelegramNotifier**.send_alpha_alert(self, project_data)`
- *Mô tả:* Format dữ liệu dự án thành một tin nhắn đẹp mắt và gửi đi.  Args:     project_data (dict): Dictionary chứa thông tin dự án.      Returns:     bool: Tr...
- *Dòng:* 52

### ⚡ `**TelegramNotifier**.send_message(self, text, parse_mode)`
- *Mô tả:* Gửi tin nhắn thô qua Telegram.  Args:     text (str): Nội dung tin nhắn.     parse_mode (str): Định dạng tin nhắn (HTML hoặc Markdown).      Returns: ...
- *Dòng:* 22

## 📁 `airdrop_guerrilla\src\utils\proxy_manager.py`
### ⚡ `**ProxyManager**.__init__(self, proxy_list_path)`
- *Dòng:* 10

### ⚡ `**ProxyManager**._load_proxies(self)`
- *Mô tả:* Nap danh sach proxy tu file.
- *Dòng:* 19

### ⚡ `**ProxyManager**.add_proxy(self, proxy_str)`
- *Mô tả:* Them proxy moi vao danh sach (Format: http://user:pass@host:port).
- *Dòng:* 43

### ⚡ `**ProxyManager**.get_proxy_for_account(self, account_id)`
- *Mô tả:* Lay proxy gan cho account.  Su dung thuat toan hashing account_id de luon lay dung 1 proxy cho 1 acc.
- *Dòng:* 31

## 📁 `airdrop_guerrilla\src\utils\stealth_vault.py`
### ⚡ `**StealthVault**.__init__(self, vault_path)`
- *Dòng:* 15

### ⚡ `**StealthVault**._load_or_create_key(self)`
- *Mô tả:* Khoi tao hoac nạp key ma hoa tu Master Key he thong.
- *Dòng:* 26

### ⚡ `**StealthVault**.decrypt_and_retrieve(self, alias)`
- *Mô tả:* Giai ma va lay du lieu.
- *Dòng:* 48

### ⚡ `**StealthVault**.encrypt_and_store(self, alias, secret_data)`
- *Mô tả:* Ma hoa va luu tru du lieu.
- *Dòng:* 40

## 📁 `projects\FlowNSFW-main\scripts\demo.py`
### ⚡ `extract_frames_from_video(video_path, max_frames)`
- *Mô tả:* Extract frames from video file.
- *Dòng:* 22

### ⚡ `load_frame_sequence(frame_dir)`
- *Mô tả:* Load frames from directory.
- *Dòng:* 38

### ⚡ `main()`
- *Dòng:* 151

### ⚡ `preprocess_frames(frames, target_size)`
- *Mô tả:* Convert frames to model input tensor.
- *Dòng:* 53

### ⚡ `print_result(result, video_name)`
- *Mô tả:* Pretty print inference result.
- *Dòng:* 119

### ⚡ `sliding_window_inference(model, frames_t, clip_len, stride, device)`
- *Mô tả:* Run sliding window inference.
- *Dòng:* 69

## 📁 `projects\FlowNSFW-main\scripts\eval_multi_res.py`
### ⚡ `eval_at_resolution(model, manifest, resolution, device)`
- *Mô tả:* Evaluate at a single resolution.
- *Dòng:* 19

### ⚡ `main()`
- *Dòng:* 55

## 📁 `projects\FlowNSFW-main\scripts\infer.py`
### ⚡ `draw_box(img, cx, cy, w, h, conf, cls_name, color)`
- *Mô tả:* Draw YOLO-style bounding box on image.
- *Dòng:* 32

### ⚡ `find_videos(source, min_frames)`
- *Dòng:* 21

### ⚡ `infer_video(model, frame_dir, device, clip_len, stride, draw_boxes)`
- *Mô tả:* Full sliding-window video classification + detection boxes.  Returns per-frame NSFW confidence + bounding boxes from detection head.
- *Dòng:* 49

### ⚡ `main()`
- *Dòng:* 124

## 📁 `projects\FlowNSFW-main\scripts\train.py`
### ⚡ `_cosine_lr(step, max_step, warmup, base_lr)`
- *Dòng:* 60

### ⚡ `_set_lr(opt, lr)`
- *Dòng:* 67

### ⚡ `collate_simple(batch)`
- *Mô tả:* Collate for balanced batch — all same resolution, handle boxes as list.
- *Dòng:* 42

### ⚡ `main()`
- *Dòng:* 72

## 📁 `projects\ai_trading_agent\backtest\backtester.py`
### ⚡ `run_multi_asset_backtest(initial_capital, max_days, trading_fee)`
- *Mô tả:* Backtest chiến lược Multi-Agent (Portfolio Allocation) so với Benchmark (HODL BTC).
- *Dòng:* 27

## 📁 `projects\ai_trading_agent\backtest\offline_backtest.py`
### ⚡ `**OfflineBacktester**.__enter__(self)`
- *Dòng:* 57

### ⚡ `**OfflineBacktester**.__exit__(self, exc_type, exc_val, exc_tb)`
- *Dòng:* 60

### ⚡ `**OfflineBacktester**.__init__(self, db_path)`
- *Mô tả:* Initialize backtester  Args:     db_path: Path to trading_market.db (auto-detected if None)
- *Dòng:* 27

### ⚡ `**OfflineBacktester**.backtest(self, ticker, strategy, start_date, end_date, days, initial_capital)`
- *Mô tả:* Run backtest simulation  Args:     ticker: Ticker symbol     strategy: Strategy type     start_date: Start date     end_date: End date     days: Numbe...
- *Dòng:* 159

### ⚡ `**OfflineBacktester**.close(self)`
- *Mô tả:* Close database connection
- *Dòng:* 51

### ⚡ `**OfflineBacktester**.compare_strategies(self, ticker, days)`
- *Mô tả:* Compare multiple strategies  Args:     ticker: Ticker symbol     days: Number of days      Returns:     DataFrame with comparison results
- *Dòng:* 289

### ⚡ `**OfflineBacktester**.connect(self)`
- *Mô tả:* Connect to database
- *Dòng:* 46

### ⚡ `**OfflineBacktester**.generate_signals(self, df, strategy)`
- *Mô tả:* Generate trading signals based on indicators  Args:     df: DataFrame with OHLCV + indicators     strategy: Strategy type ('rsi', 'macd', 'bb', 'combi...
- *Dòng:* 103

### ⚡ `**OfflineBacktester**.get_historical_data(self, ticker, start_date, end_date, days)`
- *Mô tả:* Get historical OHLCV data with indicators  Args:     ticker: Ticker symbol (e.g., "BTC_USD")     start_date: Start date (YYYY-MM-DD)     end_date: End...
- *Dòng:* 63

### ⚡ `main()`
- *Mô tả:* Run offline backtest demo
- *Dòng:* 345

### ⚡ `**OfflineBacktester**.print_results(self, results)`
- *Mô tả:* Print backtest results in a formatted way
- *Dòng:* 322

## 📁 `projects\ai_trading_agent\src\analysis_to_social.py`
### ⚡ `**AnalysisAgent**.__init__(self)`
- *Dòng:* 16

### ⚡ `**AnalysisAgent**._ai_handler(self, tech_data)`
- *Dòng:* 22

### ⚡ `**AnalysisAgent**._logic_handler(self, data)`
- *Dòng:* 19

## 📁 `projects\ai_trading_agent\src\analytics.py`
### ⚡ `**Analytics**.__init__(self)`
- *Dòng:* 32

### ⚡ `**Analytics**._ai_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 38

### ⚡ `**Analytics**._ensure_log_file(self)`
- *Dòng:* 46

### ⚡ `**Analytics**._logic_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 42

### ⚡ `**Analytics**.get_summary(self)`
- *Mô tả:* Tính toán tổng hợp hiệu suất.
- *Dòng:* 83

### ⚡ `**Analytics**.log_api_cost(self, service, tokens, estimated_cost)`
- *Mô tả:* Ghi nhận chi phí sử dụng API (LLM, Data).
- *Dòng:* 57

### ⚡ `**Analytics**.log_execution_time(self, task_name, start_time)`
- *Mô tả:* Ghi nhận thời gian thực thi của một task.
- *Dòng:* 51

### ⚡ `**Analytics**.log_trade_performance(self, trade_data)`
- *Mô tả:* Ghi nhận kết quả giao dịch. trade_data: {     'timestamp': '...',     'ticker': 'BTC-USD',     'action': 'BUY/SELL',     'price': 50000,     'pnl': 10...
- *Dòng:* 61

## 📁 `projects\ai_trading_agent\src\binance_executor.py`
### ⚡ `**BinanceExecutor**.__init__(self)`
- *Dòng:* 24

### ⚡ `**BinanceExecutor**._ai_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent - Không dùng trực tiếp LLM tại đây.
- *Dòng:* 53

### ⚡ `**BinanceExecutor**._calculate_smart_position_sizing(self, base_weight, confidence, volatility)`
- *Mô tả:* Tính toán Position Sizing thông minh.
- *Dòng:* 118

### ⚡ `**BinanceExecutor**._get_latest_atr(self, coin)`
- *Mô tả:* Lấy giá trị ATR_14 mới nhất từ database.
- *Dòng:* 97

### ⚡ `**BinanceExecutor**._logic_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 57

### ⚡ `**BinanceExecutor**.execute_allocation(self, allocation_dict, confidence)`
- *Mô tả:* Thực thi rebalance danh mục.
- *Dòng:* 124

### ⚡ `**BinanceExecutor**.get_current_portfolio(self)`
- *Mô tả:* Lấy số dư hiện tại trên sàn.
- *Dòng:* 61

## 📁 `projects\ai_trading_agent\src\config.py`
### ⚡ `**Config**.validate(cls)`
- *Mô tả:* Kiểm tra các biến môi trường quan trọng.
- *Dòng:* 47

## 📁 `projects\ai_trading_agent\src\data_fetcher.py`
### ⚡ `fetch_crypto_data(tickers, start_date, end_date)`
- *Mô tả:* Kéo dữ liệu OHLCV lịch sử từ Yahoo Finance và lưu vào SQLite. Bổ sung lấy Fear & Greed Index. IMPROVEMENT: Data Caching - chỉ fetch data mới nhất (Inc...
- *Dòng:* 57

### ⚡ `fetch_fear_and_greed(limit)`
- *Mô tả:* Lấy chỉ số Fear & Greed Index từ API của Alternative.me.
- *Dòng:* 34

### ⚡ `get_trade_tickers()`
- *Mô tả:* Lấy danh sách các cặp giao dịch từ cấu hình.
- *Dòng:* 30

## 📁 `projects\ai_trading_agent\src\fundamental_fetcher.py`
### ⚡ `**FundamentalAnalyzer**.__init__(self)`
- *Dòng:* 25

### ⚡ `**FundamentalAnalyzer**._ai_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 28

### ⚡ `**FundamentalAnalyzer**._logic_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 32

### ⚡ `**FundamentalAnalyzer**.generate_fundamental_report(self, tickers)`
- *Mô tả:* Tạo báo cáo Phân tích Cơ bản dạng chuỗi để nạp cho AI LangGraph.
- *Dòng:* 81

### ⚡ `**FundamentalAnalyzer**.get_fundamental_data(self, symbol)`
- *Mô tả:* Lấy các chỉ số tài chính cơ bản của một tài sản. Với Crypto (BTC-USD, ETH-USD), yfinance có giới hạn dữ liệu cơ bản, nhưng vẫn có thể lấy được Market ...
- *Dòng:* 36

## 📁 `projects\ai_trading_agent\src\funding_rate.py`
### ⚡ `**FundingRateMonitor**.__init__(self)`
- *Mô tả:* Initialize Funding Rate Monitor
- *Dòng:* 19

### ⚡ `**FundingRateMonitor**.get_avg_funding_rate(self, symbol)`
- *Mô tả:* Calculate average funding rate across exchanges  Args:     symbol: Crypto symbol (e.g., "BTC", "ETH", "SOL")      Returns:     Dict with average fundi...
- *Dòng:* 79

### ⚡ `**FundingRateMonitor**.get_funding_rate_history(self, symbol, interval, limit)`
- *Mô tả:* Get historical funding rates  Args:     symbol: Crypto symbol     interval: Time interval (1h, 4h, 1d)     limit: Number of data points      Returns: ...
- *Dòng:* 207

### ⚡ `**FundingRateMonitor**.get_funding_rate_summary(self, symbols)`
- *Mô tả:* Get formatted summary of funding rates for AI Agent  Args:     symbols: List of symbols to monitor      Returns:     Formatted string with funding rat...
- *Dòng:* 158

### ⚡ `**FundingRateMonitor**.get_funding_rates(self, symbol)`
- *Mô tả:* Get current funding rates for a specific symbol  Args:     symbol: Crypto symbol (e.g., "BTC", "ETH", "SOL")      Returns:     DataFrame with funding ...
- *Dòng:* 24

### ⚡ `main()`
- *Mô tả:* Test Funding Rate Monitor
- *Dòng:* 265

## 📁 `projects\ai_trading_agent\src\github_fetcher.py`
### ⚡ `fetch_github_trending_crypto(days, limit)`
- *Mô tả:* Lấy danh sách các repository liên quan đến crypto/blockchain  đang trending (nhiều sao nhất) trên GitHub trong `days` ngày qua.
- *Dòng:* 4

## 📁 `projects\ai_trading_agent\src\langgraph_agent.py`
### ⚡ `**MultiAgentTradingSystem**.__init__(self)`
- *Dòng:* 48

### ⚡ `**GenericAgent**._ai_handler(self)`
- *Dòng:* 42

### ⚡ `**MultiAgentTradingSystem**._ai_handler(self)`
- *Mô tả:* Implement abstract method from BaseAgent
- *Dòng:* 61

### ⚡ `**MultiAgentTradingSystem**._build_graph(self)`
- *Dòng:* 189

### ⚡ `**MultiAgentTradingSystem**._fundamental_node(self, state)`
- *Dòng:* 112

### ⚡ `**MultiAgentTradingSystem**._init_node(self, state)`
- *Mô tả:* Node khởi tạo để kích hoạt luồng Fan-out
- *Dòng:* 69

### ⚡ `**GenericAgent**._logic_handler(self)`
- *Dòng:* 44

### ⚡ `**MultiAgentTradingSystem**._logic_handler(self)`
- *Mô tả:* Implement abstract method from BaseAgent
- *Dòng:* 65

### ⚡ `**MultiAgentTradingSystem**._risk_manager_node(self, state)`
- *Dòng:* 127

### ⚡ `**MultiAgentTradingSystem**._sentiment_node(self, state)`
- *Dòng:* 96

### ⚡ `**MultiAgentTradingSystem**._technical_node(self, state)`
- *Dòng:* 77

### ⚡ `**MultiAgentTradingSystem**.analyze_and_trade(self, multi_asset_data_str, current_portfolio, news_list, fundamental_data, historical_data_df)`
- *Dòng:* 220

## 📁 `projects\ai_trading_agent\src\live_advisor.py`
### ⚡ `get_latest_market_data(tickers, days)`
- *Mô tả:* Lấy dữ liệu đa tài sản từ SQLite.  Args:     tickers (list, optional): Danh sách các cặp coin cần lấy dữ liệu. Mặc định là None.     days (int, option...
- *Dòng:* 45

### ⚡ `get_latest_news(ticker)`
- *Mô tả:* Lấy tin tức mới nhất từ CoinTelegraph để phân tích Sentiment.  Args:     ticker (str): Tên coin (hiện tại không ảnh hưởng vì lấy tin chung).      Retu...
- *Dòng:* 83

### ⚡ `run_live_advisor()`
- *Mô tả:* Hàm thực thi chính của Live Advisor. Kéo dữ liệu, tin tức, gọi hệ thống Multi-Agent đánh giá và thực thi lệnh (hoặc mô phỏng).
- *Dòng:* 98

## 📁 `projects\ai_trading_agent\src\mini_backtest.py`
### ⚡ `get_cached_prices(coins, days)`
- *Dòng:* 11

### ⚡ `run_mini_backtest(allocation_dict, days)`
- *Mô tả:* Chạy mini-backtest trên dữ liệu `days` ngày qua với tỷ trọng `allocation_dict`. Trả về Dict chứa: - total_return_pct: % lợi nhuận - sharpe_ratio: Shar...
- *Dòng:* 52

## 📁 `projects\ai_trading_agent\src\ml_prediction.py`
### ⚡ `**LeftBrainPredictor**.__init__(self)`
- *Dòng:* 2

### ⚡ `**LeftBrainPredictor**.predict(self, df)`
- *Dòng:* 5

## 📁 `projects\ai_trading_agent\src\news_scraper.py`
### ⚡ `fetch_cointelegraph_news(limit)`
- *Mô tả:* Cào tin tức mới nhất từ RSS Feed của CoinTelegraph. Hoạt động cực nhanh và không bị block như cào web thông thường.
- *Dòng:* 5

## 📁 `projects\ai_trading_agent\src\portfolio_optimizer.py`
### ⚡ `calculate_portfolio_performance(weights, returns)`
- *Mô tả:* Tính toán lợi nhuận và rủi ro của danh mục.
- *Dòng:* 51

### ⚡ `calculate_risk_parity_weights(returns)`
- *Mô tả:* Tính toán tỷ trọng theo phương pháp Risk Parity (Cân bằng rủi ro). Mục tiêu: Đóng góp rủi ro của mỗi tài sản vào danh mục là bằng nhau.
- *Dòng:* 64

### ⚡ `get_historical_prices(tickers, days)`
- *Mô tả:* Lấy dữ liệu giá đóng cửa lịch sử từ DB.
- *Dòng:* 21

### ⚡ `negative_sharpe_ratio(weights, returns, risk_free_rate)`
- *Mô tả:* Hàm mục tiêu để minimize (tìm Sharpe cao nhất).
- *Dòng:* 57

### ⚡ `optimize_portfolio(tickers, days, method)`
- *Mô tả:* Thực hiện tối ưu hóa danh mục. Hỗ trợ MPT (Sharpe) và Risk Parity.
- *Dòng:* 74

## 📁 `projects\ai_trading_agent\src\profit_harvester.py`
### ⚡ `**ProfitHarvester**.__init__(self, trailing_percent, target_profit_levels)`
- *Dòng:* 10

### ⚡ `**ProfitHarvester**.open_position(self, symbol, entry_price)`
- *Dòng:* 43

### ⚡ `**ProfitHarvester**.update_position(self, symbol, current_price)`
- *Mô tả:* Cap nhat trang thai vi the va kiem tra diem chot loi.
- *Dòng:* 15

## 📁 `projects\ai_trading_agent\src\social_scraper.py`
### ⚡ `async fetch_reddit_crypto_sentiment(limit)`
- *Mô tả:* Cào các hot posts từ r/CryptoCurrency để phân tích Social Sentiment. Không cần API Key, chỉ cần custom User-Agent.
- *Dòng:* 4

## 📁 `projects\ai_trading_agent\src\technical_engine.py`
### ⚡ `**TechnicalEngine**.__init__(self)`
- *Dòng:* 12

### ⚡ `**TechnicalEngine**.analyze_trend(self, df)`
- *Mô tả:* Phân tích theo chuẩn Minervini Stage 2 (Uptrend mạnh). Sử dụng Vectorization để đạt hiệu năng tối đa.
- *Dòng:* 15

## 📁 `projects\ai_trading_agent\src\telegram_intelligence.py`
### ⚡ `**TelegramIntelligenceAgent**.__init__(self)`
- *Dòng:* 16

### ⚡ `**TelegramIntelligenceAgent**._ai_handler(self, messages)`
- *Dòng:* 22

### ⚡ `**TelegramIntelligenceAgent**._logic_handler(self, data)`
- *Dòng:* 19

### ⚡ `async main()`
- *Dòng:* 35

## 📁 `projects\ai_trading_agent\src\validation_gate.py`
### ⚡ `**ValidationGate**.__init__(self)`
- *Dòng:* 11

### ⚡ `**ValidationGate**.check_data_integrity(self, ticker, current_price)`
- *Mô tả:* [VULN-003] Kiểm tra tính toàn vẹn của dữ liệu (Sanity Check). Ngăn chặn ChaosMonkey tiêm giá ảo vào Database.
- *Dòng:* 19

### ⚡ `**ValidationGate**.validate_proposal(self, df, proposal, market_price)`
- *Mô tả:* Kiểm tra đề xuất lệnh dựa trên dữ liệu 7 ngày và Slippage Guard.
- *Dòng:* 32

## 📁 `projects\ai_trading_agent\src\whale_alert.py`
### ⚡ `**WhaleAlertMonitor**.__init__(self, api_key)`
- *Mô tả:* Initialize Whale Alert Monitor  Args:     api_key: Whale Alert API key (get from whale-alert.io)             If None, will try to get from Config
- *Dòng:* 24

### ⚡ `**WhaleAlertMonitor**.get_exchange_inflow_outflow(self, asset, min_value, hours)`
- *Mô tả:* Calculate net flow to/from exchanges  Args:     asset: Crypto asset (e.g., "bitcoin", "ethereum", "solana")     min_value: Minimum transaction value i...
- *Dòng:* 142

### ⚡ `**WhaleAlertMonitor**.get_transactions(self, min_value, asset, hours)`
- *Mô tả:* Get recent large transactions  Args:     min_value: Minimum transaction value in USD (default: 500k)     asset: Specific crypto asset (e.g., "bitcoin"...
- *Dòng:* 41

### ⚡ `**WhaleAlertMonitor**.get_whale_alert_summary(self, assets, min_value, hours)`
- *Mô tả:* Get formatted summary of whale activity for AI Agent  Args:     assets: List of assets to monitor     min_value: Minimum transaction value in USD     ...
- *Dòng:* 184

### ⚡ `main()`
- *Mô tả:* Test Whale Alert Monitor
- *Dòng:* 239

## 📁 `projects\ai_trading_agent\src\whale_tracker.py`
### ⚡ `**WhaleTrackerAgent**.__init__(self)`
- *Dòng:* 4

### ⚡ `**WhaleTrackerAgent**._ai_handler(self, state)`
- *Dòng:* 7

### ⚡ `**WhaleTrackerAgent**._logic_handler(self, state)`
- *Dòng:* 10

### ⚡ `**WhaleTrackerAgent**.execute(self, alerts)`
- *Dòng:* 16

### ⚡ `**WhaleTrackerAgent**.scrape_whale_data(self)`
- *Dòng:* 13

## 📁 `projects\ai_trading_agent\tools\generate_performance_report.py`
### ⚡ `generate_markdown_report()`
- *Mô tả:* Tạo báo cáo hiệu suất từ dữ liệu Paper Trade trong Database.
- *Dòng:* 9

## 📁 `projects\asset_audit_taskforce\src\arb_session.py`
### ⚡ `**ArchitectureReconstructionBoard**.__init__(self)`
- *Dòng:* 23

### ⚡ `**ArchitectureReconstructionBoard**.run_full_session(self)`
- *Dòng:* 31

## 📁 `projects\asset_audit_taskforce\src\judge_executor.py`
### ⚡ `**DiskCleaner**.__init__(self)`
- *Dòng:* 8

### ⚡ `**DiskCleaner**._format_size(self, size_in_bytes)`
- *Mô tả:* Định dạng byte sang MB/GB cho dễ nhìn
- *Dòng:* 19

### ⚡ `**DiskCleaner**._get_dir_size(self, path)`
- *Mô tả:* Lấy kích thước một thư mục
- *Dòng:* 29

### ⚡ `**DiskCleaner**.clean_dev_caches(self)`
- *Mô tả:* Gọi CLI để dọn cache của pip, uv, npm
- *Dòng:* 72

### ⚡ `**DiskCleaner**.clean_docker(self)`
- *Mô tả:* Xóa Docker images/containers dangling
- *Dòng:* 95

### ⚡ `**DiskCleaner**.clean_temp_folders(self)`
- *Mô tả:* Xóa các thư mục Temp của Windows
- *Dòng:* 42

### ⚡ `**DiskCleaner**.run(self)`
- *Dòng:* 117

## 📁 `projects\auto_affiliate_video\src\affiliate_manager.py`
### ⚡ `**AffiliateManager**.__init__(self)`
- *Dòng:* 8

### ⚡ `**AffiliateManager**.generate_affiliate_link(self, product_url)`
- *Mô tả:* Tạo link rút gọn Affiliate thông qua API của AccessTrade. Nếu API lỗi hoặc thiếu cấu hình, trả về link dự phòng.
- *Dòng:* 13

## 📁 `projects\auto_affiliate_video\src\auto_uploader.py`
### ⚡ `**AutoUploader**.__init__(self)`
- *Dòng:* 9

### ⚡ `**AutoUploader**.upload_to_tiktok(self, video_path, caption)`
- *Dòng:* 12

## 📁 `projects\auto_affiliate_video\src\main.py`
### ⚡ `main()`
- *Mô tả:* Hàm main điều phối quá trình tự động tạo video Affiliate.
- *Dòng:* 30

## 📁 `projects\auto_affiliate_video\src\pexel_client.py`
### ⚡ `**PexelClient**._get_best_quality_link(self, video_links)`
- *Mô tả:* Selects the best quality video link that is under a certain size if needed.
- *Dòng:* 68

### ⚡ `**PexelClient**.find_and_download_video(self, query, output_path)`
- *Mô tả:* Searches for a video on Pexels and downloads the most relevant one.  Args:     query (str): The search term for the video.     output_path (str): The ...
- *Dòng:* 18

## 📁 `projects\auto_affiliate_video\src\scheduler.py`
### ⚡ `job()`
- *Dòng:* 7

## 📁 `projects\auto_affiliate_video\src\script_generator.py`
### ⚡ `**ScriptGenerator**.__init__(self)`
- *Dòng:* 18

### ⚡ `**ScriptGenerator**._ai_handler(self, state)`
- *Dòng:* 21

### ⚡ `**ScriptGenerator**._logic_handler(self, state)`
- *Dòng:* 24

### ⚡ `**ScriptGenerator**.generate_short_video_script(self, product_name, key_features)`
- *Mô tả:* Dùng OpenAI/Gemini để viết kịch bản video ngắn (dưới 60s) cho TikTok/Shorts. Áp dụng quy tắc Hook của sách Zero to Hero và Sức mạnh Ngôn từ.
- *Dòng:* 27

## 📁 `projects\auto_affiliate_video\src\tiktok_api_uploader.py`
### ⚡ `**TikTokApiUploader**.__init__(self)`
- *Dòng:* 9

### ⚡ `**TikTokApiUploader**.upload_to_tiktok(self, video_path, caption)`
- *Dòng:* 15

## 📁 `projects\auto_affiliate_video\src\tts_engine.py`
### ⚡ `**TTSEngine**.__init__(self, voice)`
- *Dòng:* 15

### ⚡ `**TTSEngine**._apply_audio_effects(self, audio_path)`
- *Mô tả:* Ap dung cac hieu ung am thanh chuyen nghiep.
- *Dòng:* 33

### ⚡ `async **TTSEngine**.generate_audio(self, text, filename)`
- *Mô tả:* Sinh ra file mp3 tu van ban bang Edge-TTS.
- *Dòng:* 20

## 📁 `projects\auto_affiliate_video\src\vector_memory.py`
### ⚡ `**VectorMemory**.__init__(self, db_path)`
- *Dòng:* 10

### ⚡ `**VectorMemory**.embed_and_store(self, document_id, content, metadata)`
- *Mô tả:* Tạo embedding và lưu nội dung vào Vector DB.
- *Dòng:* 24

### ⚡ `**VectorMemory**.ingest_chronicles(self, file_path)`
- *Mô tả:* Đọc và băm nhỏ file JARVIS_CHRONICLES.md để nạp vào trí nhớ.
- *Dòng:* 57

### ⚡ `**VectorMemory**.query_similar_context(self, query_text, n_results)`
- *Mô tả:* Truy xuất N nội dung tương tự nhất dựa trên câu truy vấn.
- *Dòng:* 41

## 📁 `projects\auto_affiliate_video\src\video_editor.py`
### ⚡ `**VideoEditor**.__init__(self)`
- *Dòng:* 7

### ⚡ `**VideoEditor**.create_short_video(self, audio_path, background_video_path, output_filename)`
- *Mô tả:* Ghép Audio AI vào Video Background. Tự động cắt video nền cho bằng với độ dài của Audio. Lưu ý: MoviePy có thể chạy chậm trên i3, nên render độ phân g...
- *Dòng:* 16

## 📁 `projects\auto_affiliate_video\src\video_telemetry.py`
### ⚡ `**VideoTelemetry**.__init__(self, log_file)`
- *Dòng:* 8

### ⚡ `**VideoTelemetry**._save_to_disk(self)`
- *Dòng:* 34

### ⚡ `**VideoTelemetry**.log_event(self, step_name, start_time, end_time)`
- *Dòng:* 19

### ⚡ `measure_latency(step_name)`
- *Mô tả:* Decorator to automatically measure the latency of a function and log it.
- *Dòng:* 61

### ⚡ `**VideoTelemetry**.start_run(self, run_id)`
- *Dòng:* 14

## 📁 `projects\auto_x_bot\src\browser_bot.py`
### ⚡ `**XBrowserBot**.__init__(self, profile_name)`
- *Dòng:* 27

### ⚡ `async **XBrowserBot**.interact_with_trends(self, keywords)`
- *Mô tả:* Tuong tac voi cac xu huong de tang uy tin account.
- *Dòng:* 64

### ⚡ `async **XBrowserBot**.post_tweet_browser(self, content)`
- *Mô tả:* Dang tweet bang cach dieu khien trinh duyet.
- *Dòng:* 31

## 📁 `projects\auto_x_bot\src\content_generator.py`
### ⚡ `**ContentGenerator**.__init__(self)`
- *Dòng:* 12

### ⚡ `**ContentGenerator**.generate_crypto_tweet(self, news_items)`
- *Mô tả:* Dựa vào danh sách tin tức, suy nghĩ ra 1 dòng Tweet duy nhất cực kỳ viral, chuẩn phong cách Crypto Twitter (có emoji, hashtags #Crypto #Bitcoin). Khôn...
- *Dòng:* 19

## 📁 `projects\auto_x_bot\src\social_coordinator.py`
### ⚡ `async social_mining_cycle()`
- *Dòng:* 27

## 📁 `projects\gemini_cli\core\client.py`
### ⚡ `async **GeminiClient**.__aenter__(self)`
- *Mô tả:* Async context manager entry.
- *Dòng:* 64

### ⚡ `async **GeminiClient**.__aexit__(self, exc_type, exc_val, exc_tb)`
- *Mô tả:* Async context manager exit.
- *Dòng:* 73

### ⚡ `**GeminiClient**.__init__(self, config)`
- *Mô tả:* Initialize Gemini client.  Args:     config: Configuration object with API credentials.
- *Dòng:* 54

### ⚡ `async **GeminiClient**.chat(self, prompt, model)`
- *Mô tả:* Send a chat prompt and return complete response (non-streaming).  Args:     prompt: User's prompt text.     model: Model name (uses config default if ...
- *Dòng:* 203

### ⚡ `async **GeminiClient**.stream_chat(self, prompt, model)`
- *Mô tả:* Send a chat prompt and stream the response.  Args:     prompt: User's prompt text.     model: Model name (uses config default if None).  Yields:     C...
- *Dòng:* 78

## 📁 `projects\gemini_cli\core\config.py`
### ⚡ `**Config**.__init__(self, env_file)`
- *Mô tả:* Initialize configuration by loading environment variables.  Args:     env_file: Path to .env file. If None, searches in parent directories.  Raises:  ...
- *Dòng:* 29

### ⚡ `**Config**.__repr__(self)`
- *Mô tả:* String representation (safe - hides API key).
- *Dòng:* 118

### ⚡ `**Config**._validate(self)`
- *Mô tả:* Validate that all required environment variables are set.
- *Dòng:* 50

### ⚡ `**Config**.api_key(self)`
- *Mô tả:* Get Gemini API key from environment.  Returns:     API key string or None if not set.
- *Dòng:* 64

### ⚡ `**Config**.base_url(self)`
- *Mô tả:* Get Gemini API base URL from environment.  Returns:     Base URL string or default if not set.
- *Dòng:* 74

### ⚡ `**Config**.get_headers(self)`
- *Mô tả:* Get HTTP headers for API requests.  Returns:     Dictionary of HTTP headers.
- *Dòng:* 106

### ⚡ `**Config**.model(self)`
- *Mô tả:* Get default model name.  Returns:     Model name string.
- *Dòng:* 87

### ⚡ `**Config**.timeout(self)`
- *Mô tả:* Get request timeout in seconds.  Returns:     Timeout value in seconds.
- *Dòng:* 97

## 📁 `projects\godot_translator\core\cyber_security.py`
### ⚡ `**IntegrityGuard**.__init__(self, target_files)`
- *Dòng:* 13

### ⚡ `**InjectionGuard**.__init__(self)`
- *Dòng:* 57

### ⚡ `**IntegrityGuard**._calculate_hash(self, file_path)`
- *Mô tả:* Tính toán mã băm SHA-256 của file.
- *Dòng:* 18

### ⚡ `**IntegrityGuard**.deploy_logic_mine(self)`
- *Mô tả:* Triển khai 'Mìn logic' - Tự hủy phiên làm việc nếu vi phạm tính toàn vẹn.
- *Dòng:* 46

### ⚡ `**InjectionGuard**.is_safe(self, user_input)`
- *Mô tả:* Kiem tra xem input cua nguoi dung co an toan khong.
- *Dòng:* 74

### ⚡ `**IntegrityGuard**.record_baseline(self)`
- *Mô tả:* Ghi nhận mã băm gốc của các file quan trọng.
- *Dòng:* 26

### ⚡ `**InjectionGuard**.sanitize_input(self, user_input)`
- *Mô tả:* Lam sach input neu can thiet.
- *Dòng:* 88

### ⚡ `**IntegrityGuard**.verify_integrity(self)`
- *Mô tả:* Kiểm tra xem file có bị thay đổi không.
- *Dòng:* 33

## 📁 `projects\godot_translator\core\decompiler.py`
### ⚡ `**GodotDecompiler**.__init__(self, tool_path)`
- *Dòng:* 16

### ⚡ `**GodotDecompiler**.decompile_pck(self, pck_path, output_dir)`
- *Mô tả:* Decompile a .pck file using GDRE Tools CLI.
- *Dòng:* 19

## 📁 `projects\godot_translator\core\extractor.py`
### ⚡ `**GodotExtractor**.__init__(self, target_dir)`
- *Dòng:* 19

### ⚡ `**GodotExtractor**.extract_from_file(self, file_path)`
- *Mô tả:* Extract Japanese strings from a single file based on its type.
- *Dòng:* 28

### ⚡ `**GodotExtractor**.scan_files(self)`
- *Mô tả:* Recursively scan for .gd and .tscn files.
- *Dòng:* 22

## 📁 `projects\godot_translator\core\gdre_downloader.py`
### ⚡ `download_gdre_tools(target_dir)`
- *Dòng:* 17

## 📁 `projects\godot_translator\core\injector.py`
### ⚡ `**GodotInjector**.__init__(self, target_root, output_dir)`
- *Dòng:* 13

### ⚡ `**GodotInjector**.inject(self, file_path, translations)`
- *Mô tả:* Replace Japanese strings and save in the mirrored structure, while cleaning .remap/.gdc files.
- *Dòng:* 18

## 📁 `projects\godot_translator\core\pack_manager.py`
### ⚡ `**PackManager**.__init__(self, temp_dir)`
- *Dòng:* 17

### ⚡ `**PackManager**.cleanup_temp(self)`
- *Mô tả:* Dọn dẹp rác (Garbage Collection) khi xong hoặc khi lỗi.
- *Dòng:* 331

### ⚡ `**PackManager**.detect_godot_version(self, file_path)`
- *Mô tả:* Kiểm tra Magic Bytes để nhận diện Godot PCK format.
- *Dòng:* 22

### ⚡ `**PackManager**.repack(self, original_exe_path, modified_dir, key, progress_callback)`
- *Mô tả:* Đóng gói lại thư mục đã dịch thành file game mới sử dụng GDRE Tools.
- *Dòng:* 159

### ⚡ `**PackManager**.test_run(self, game_exe_path, extract_dir)`
- *Mô tả:* Khởi chạy game (Sandbox Playtest) không chặn UI chính.
- *Dòng:* 110

### ⚡ `**PackManager**.unpack(self, game_file_path, progress_callback, key)`
- *Mô tả:* Giải nén file .exe hoặc .pck ra thư mục tạm. Hỗ trợ giải mã với Encryption Key (nếu có).
- *Dòng:* 36

## 📁 `projects\godot_translator\core\translator.py`
### ⚡ `**GodotTranslator**.__init__(self, model_name, api_key)`
- *Dòng:* 26

### ⚡ `**GodotTranslator**._ai_handler(self, texts)`
- *Mô tả:* Optimal Path: Use LLM to translate strings.
- *Dòng:* 39

### ⚡ `**GodotTranslator**._logic_handler(self, texts)`
- *Mô tả:* Fallback Path: Return original texts (no translation) if AI fails.
- *Dòng:* 35

### ⚡ `**GodotTranslator**.translate_batch(self, texts)`
- *Mô tả:* Execute translation with batching.
- *Dòng:* 65

## 📁 `projects\godot_translator\utils\ui_helper.py`
### ⚡ `ui_error_guard(func)`
- *Mô tả:* Decorator de bảo vệ UI Streamlit khỏi các lỗi Backend. Thay vì hiện Traceback, nó hiện thông báo thân thiện và ghi log ngầm.
- *Dòng:* 7

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\ai_agent.py`
### ⚡ `**AIService**.__init__(self, key_manager)`
- *Dòng:* 47

### ⚡ `**AIService**._get_cached_response(self, prompt, model)`
- *Mô tả:* Kiểm tra xem câu hỏi này đã có trong cache chưa.
- *Dòng:* 58

### ⚡ `**AIService**._update_cache(self, prompt, model, response)`
- *Mô tả:* Lưu câu trả lời vào cache.
- *Dòng:* 70

### ⚡ `ask_jarvis(prompt)`
- *Mô tả:* Hàm giao tiếp cơ bản với Jarvis.
- *Dòng:* 118

### ⚡ `evaluate_evolution(current_profile, completed_tasks)`
- *Mô tả:* Đánh giá nhiệm vụ để tính XP/HP (RPG System). Có xử lý JSON an toàn.
- *Dòng:* 127

### ⚡ `**AIService**.generate_response(self, prompt, model)`
- *Mô tả:* Hàm chính để tạo phản hồi (Có Cache + Đồng bộ Fallback Chain).
- *Dòng:* 82

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\ai_agent_fixed.py`
### ⚡ `**CircuitBreaker**.__init__(self, failure_threshold, open_duration, half_open_max_requests)`
- *Dòng:* 79

### ⚡ `**SingleFlightLRUCache**.__init__(self, max_items, max_memory_mb, ttl)`
- *Dòng:* 224

### ⚡ `**AIService**.__init__(self, key_manager)`
- *Dòng:* 444

### ⚡ `**AIService**._call_llm_api(self, prompt, model)`
- *Mô tả:* Call Gemini API with retry logic.  This is wrapped by Circuit Breaker to prevent death spirals.
- *Dòng:* 461

### ⚡ `**SingleFlightLRUCache**._fetch_and_cache(self, cache_key, fetch_fn)`
- *Mô tả:* Fetch from API and store in cache.
- *Dòng:* 361

### ⚡ `**SingleFlightLRUCache**._get_from_cache(self, cache_key)`
- *Mô tả:* Get from cache if exists and not expired.
- *Dòng:* 341

### ⚡ `**CircuitBreaker**._get_remaining_cooldown(self)`
- *Mô tả:* Get remaining cooldown time in seconds.
- *Dòng:* 151

### ⚡ `**CircuitBreaker**._on_failure(self)`
- *Mô tả:* Handle failed request.
- *Dòng:* 177

### ⚡ `**CircuitBreaker**._on_success(self)`
- *Mô tả:* Handle successful request.
- *Dòng:* 166

### ⚡ `**SingleFlightLRUCache**._remove_entry(self, cache_key)`
- *Mô tả:* Remove entry and update memory counter.
- *Dòng:* 400

### ⚡ `**CircuitBreaker**._should_attempt_reset(self)`
- *Mô tả:* Check if enough time has passed to try HALF_OPEN.
- *Dòng:* 143

### ⚡ `**CircuitBreaker**._transition_to_half_open(self)`
- *Mô tả:* Transition from OPEN to HALF_OPEN.
- *Dòng:* 160

### ⚡ `ask_jarvis(prompt)`
- *Mô tả:* Public API: Ask Jarvis a question (Facade Pattern).  This interface remains unchanged for backward compatibility. All resilience patterns are transpar...
- *Dòng:* 562

### ⚡ `**CircuitBreaker**.call(self, func)`
- *Mô tả:* Execute function with circuit breaker protection.  Args:     func: Function to execute     *args, **kwargs: Arguments to pass to function      Returns...
- *Dòng:* 96

### ⚡ `evaluate_evolution(current_profile, completed_tasks)`
- *Mô tả:* Evaluate tasks for XP/HP calculation (RPG System).  Unchanged from original, uses ask_jarvis internally.
- *Dòng:* 576

### ⚡ `**AIService**.generate_response(self, prompt, model)`
- *Mô tả:* Main entry point: Generate AI response with full resilience.  Flow: 1. Check Circuit Breaker state 2. Check Cache (with Single-Flight) 3. Call API if ...
- *Dòng:* 493

### ⚡ `**SingleFlightLRUCache**.get_or_fetch(self, cache_key, fetch_fn)`
- *Mô tả:* Get from cache OR wait for in-flight request OR fetch new.  This is THE SHIELD that prevents cache stampede.  Args:     cache_key: Unique identifier (...
- *Dòng:* 252

### ⚡ `**SingleFlightLRUCache**.get_stats(self)`
- *Mô tả:* Get cache statistics.
- *Dòng:* 406

### ⚡ `**CircuitBreaker**.get_status(self)`
- *Mô tả:* Get current circuit breaker status.
- *Dòng:* 196

### ⚡ `get_system_health()`
- *Mô tả:* Get system health metrics.  Useful for monitoring and debugging.
- *Dòng:* 637

### ⚡ `**AIService**.get_system_status(self)`
- *Mô tả:* Get comprehensive system health status.
- *Dòng:* 545

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\database.py`
### ⚡ `**DatabaseManager**.__init__(self, db_path)`
- *Mô tả:* Initialize the database manager.
- *Dòng:* 47

### ⚡ `**DatabaseManager**._calculate_next_review_interval(level)`
- *Dòng:* 370

### ⚡ `**DatabaseManager**._create_default_profile(self)`
- *Dòng:* 197

### ⚡ `**DatabaseManager**._execute(self, query, params)`
- *Mô tả:* Execute a write operation (INSERT/UPDATE/DELETE).
- *Dòng:* 87

### ⚡ `**DatabaseManager**._fetch_all(self, query, params)`
- *Mô tả:* Execute a query and return all rows.
- *Dòng:* 110

### ⚡ `**DatabaseManager**._fetch_one(self, query, params)`
- *Mô tả:* Execute a query and return a single row.
- *Dòng:* 99

### ⚡ `**DatabaseManager**._get_connection(self)`
- *Mô tả:* Context manager for database connections with transaction lock.
- *Dòng:* 66

### ⚡ `**DatabaseManager**._get_default_db_path()`
- *Mô tả:* Xác định đường dẫn database một cách thông minh.
- *Dòng:* 53

### ⚡ `**DatabaseManager**._init_db(self)`
- *Mô tả:* Initialize the database schema.
- *Dòng:* 123

### ⚡ `**DatabaseManager**.add_vocab(self, word, meaning, tags)`
- *Dòng:* 276

### ⚡ `add_vocab(word, meaning, tags)`
- *Dòng:* 413

### ⚡ `get_connection()`
- *Dòng:* 404

### ⚡ `get_database()`
- *Dòng:* 393

### ⚡ `**DatabaseManager**.get_due_vocab(self, limit)`
- *Dòng:* 295

### ⚡ `get_due_vocab(limit)`
- *Dòng:* 407

### ⚡ `**DatabaseManager**.get_review_candidates(self, mode, limit)`
- *Dòng:* 305

### ⚡ `get_review_candidates(mode, limit)`
- *Dòng:* 410

### ⚡ `**DatabaseManager**.get_user_profile(self)`
- *Dòng:* 191

### ⚡ `get_user_profile()`
- *Dòng:* 421

### ⚡ `init_db()`
- *Dòng:* 401

### ⚡ `**DatabaseManager**.update_user_stats(self, xp_gained, hp_change, new_status, new_class)`
- *Dòng:* 213

### ⚡ `update_user_stats(xp_gained, hp_change, new_status, new_class)`
- *Dòng:* 423

### ⚡ `**DatabaseManager**.update_vocab_mastery(self, word, is_remembered)`
- *Dòng:* 324

### ⚡ `update_vocab_mastery(word, is_remembered)`
- *Dòng:* 416

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\db_sync.py`
### ⚡ `commit_and_push_database(commit_message)`
- *Mô tả:* Commit và push database changes Returns: True nếu thành công, False nếu thất bại
- *Dòng:* 38

### ⚡ `safe_database_update(update_func, commit_msg)`
- *Mô tả:* Wrapper function để safely update database với git sync  Usage:     def my_update():         db.add_user(...)          safe_database_update(my_update,...
- *Dòng:* 91

### ⚡ `sync_database_with_git()`
- *Mô tả:* Sync database với git: pull trước khi commit để tránh conflict Returns: True nếu thành công, False nếu thất bại
- *Dòng:* 7

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\error_notifier.py`
### ⚡ `**ErrorNotifier**.__init__(self)`
- *Dòng:* 11

### ⚡ `**ErrorNotifier**._get_admin_chat_ids(self)`
- *Dòng:* 16

### ⚡ `async **ErrorNotifier**._get_bot(self)`
- *Dòng:* 22

### ⚡ `**ErrorNotifier**.notify_error_sync(self, error, context, critical)`
- *Dòng:* 62

### ⚡ `async **ErrorNotifier**.send_error_alert(self, error, context, critical)`
- *Dòng:* 31

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\google_services.py`
### ⚡ `add_task(creds, title, note)`
- *Dòng:* 27

### ⚡ `create_calendar_event(creds, summary, start_time_iso, end_time_iso, description, location)`
- *Dòng:* 149

### ⚡ `get_completed_tasks_today(creds)`
- *Dòng:* 119

### ⚡ `get_creds()`
- *Dòng:* 15

### ⚡ `get_pending_tasks(creds)`
- *Dòng:* 97

### ⚡ `get_today_events(creds)`
- *Dòng:* 47

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\key_manager.py`
### ⚡ `**KeyManager**.__init__(self, api_keys)`
- *Dòng:* 21

### ⚡ `get_global_key_manager()`
- *Mô tả:* Đọc keys từ biến môi trường và trả về KeyManager.
- *Dòng:* 79

### ⚡ `**KeyManager**.get_next_key(self)`
- *Mô tả:* Trả về key tiếp theo theo cơ chế Round-Robin, bỏ qua các key đang trong Cooldown. Sử dụng vòng lặp N lần để đảm bảo kiểm tra tất cả Keys.
- *Dòng:* 30

### ⚡ `**KeyManager**.mark_key_exhausted(self, key)`
- *Mô tả:* Đánh dấu key này đã hết hạn mức (Quota Exceeded) hoặc gặp lỗi Rate Limit. Lưu lại thời gian lỗi để tính Cooldown.
- *Dòng:* 64

### ⚡ `**KeyManager**.reset_exhausted_keys(self)`
- *Mô tả:* Xóa toàn bộ trạng thái Cooldown. Dùng khi cần reset thủ công.
- *Dòng:* 72

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\migrate_data.py`
### ⚡ `manual_restore()`
- *Dòng:* 8

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\notes.py`
### ⚡ `add_note(note_content)`
- *Mô tả:* Ghi một ghi chú mới cùng với timestamp vào file journal.
- *Dòng:* 14

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\setup_calendar.py`
### ⚡ `main()`
- *Dòng:* 14

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\telegram_bot.py`
### ⚡ `send_message(text)`
- *Dòng:* 6

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\telegram_webhook.py`
### ⚡ `**TelegramWebhookBot**.__init__(self)`
- *Dòng:* 15

### ⚡ `**TelegramWebhookBot**._setup_handlers(self)`
- *Mô tả:* Setup command and message handlers
- *Dòng:* 28

### ⚡ `async **TelegramWebhookBot**.handle_message(self, update, context)`
- *Mô tả:* Handle regular text messages
- *Dòng:* 123

### ⚡ `async **TelegramWebhookBot**.handle_photo(self, update, context)`
- *Mô tả:* Handle photo messages for calendar parsing
- *Dòng:* 35

### ⚡ `async **TelegramWebhookBot**.help_command(self, update, context)`
- *Mô tả:* Handle /help command
- *Dòng:* 108

### ⚡ `main()`
- *Mô tả:* Main entry point
- *Dòng:* 170

### ⚡ `**TelegramWebhookBot**.run(self)`
- *Mô tả:* Run bot with appropriate mode based on configuration
- *Dòng:* 162

### ⚡ `**TelegramWebhookBot**.run_polling(self)`
- *Mô tả:* Run bot with polling (for local development)
- *Dòng:* 130

### ⚡ `**TelegramWebhookBot**.run_webhook(self, listen)`
- *Mô tả:* Run bot with webhook (for production)
- *Dòng:* 148

### ⚡ `async **TelegramWebhookBot**.setup_webhook(self)`
- *Mô tả:* Setup webhook for production deployment
- *Dòng:* 135

### ⚡ `async **TelegramWebhookBot**.start_command(self, update, context)`
- *Mô tả:* Handle /start command
- *Dòng:* 101

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\vision_parser.py`
### ⚡ `**VisionParserAgent**.__init__(self)`
- *Dòng:* 22

### ⚡ `**VisionParserAgent**._ai_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent - Không dùng trong luồng này.
- *Dòng:* 26

### ⚡ `**VisionParserAgent**._logic_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent - Không dùng trong luồng này.
- *Dòng:* 30

### ⚡ `**VisionParserAgent**.parse_schedule_image(self, image_path)`
- *Mô tả:* Sử dụng BaseAgent để gọi LLM Vision (qua Local Proxy) xử lý ảnh lịch.
- *Dòng:* 34

### ⚡ `parse_schedule_image(image_path)`
- *Mô tả:* Wrapper function để không làm vỡ các module đang import hàm này.
- *Dòng:* 107

## 📁 `projects\jarvis-rpg-assistant\jarvis_core\weather_service.py`
### ⚡ `get_weather_report()`
- *Mô tả:* Lấy thông tin thời tiết hiện tại tại Đồng Nai. Return: String mô tả ngắn gọn hoặc thông báo lỗi.
- *Dòng:* 8

## 📁 `projects\jarvis-rpg-assistant\src\admin_panel.py`
### ⚡ `**JarvisAdminApp**.__init__(self, root)`
- *Dòng:* 16

### ⚡ `**JarvisAdminApp**.add_vocab(self)`
- *Dòng:* 214

### ⚡ `**JarvisAdminApp**.clear_form(self)`
- *Dòng:* 207

### ⚡ `**JarvisAdminApp**.delete_vocab(self)`
- *Dòng:* 239

### ⚡ `**JarvisAdminApp**.filter_vocab(self)`
- *Dòng:* 190

### ⚡ `**JarvisAdminApp**.load_profile(self)`
- *Dòng:* 78

### ⚡ `**JarvisAdminApp**.load_vocab_list(self, query)`
- *Dòng:* 172

### ⚡ `**JarvisAdminApp**.on_select_vocab(self, event)`
- *Dòng:* 193

### ⚡ `**JarvisAdminApp**.save_profile(self)`
- *Dòng:* 88

### ⚡ `**JarvisAdminApp**.setup_profile_tab(self)`
- *Dòng:* 43

### ⚡ `**JarvisAdminApp**.setup_vocab_tab(self)`
- *Dòng:* 114

### ⚡ `**JarvisAdminApp**.update_vocab(self)`
- *Dòng:* 227

## 📁 `projects\jarvis-rpg-assistant\src\auto_learn.py`
### ⚡ `auto_hunt_vocab()`
- *Dòng:* 16

## 📁 `projects\jarvis-rpg-assistant\src\bot_daily.py`
### ⚡ `get_vietnamese_weekday()`
- *Dòng:* 17

### ⚡ `main()`
- *Dòng:* 23

## 📁 `projects\jarvis-rpg-assistant\src\bot_evolve.py`
### ⚡ `main()`
- *Dòng:* 18

## 📁 `projects\jarvis-rpg-assistant\src\bot_teacher.py`
### ⚡ `main(mode)`
- *Mô tả:* Main teaching function. Args:     mode: 'new' để học từ mới, 'review' để ôn từ cũ
- *Dòng:* 16

## 📁 `projects\jarvis-rpg-assistant\src\fix_db.py`
### ⚡ `fix_system()`
- *Dòng:* 13

## 📁 `projects\jarvis-rpg-assistant\src\jarvis_launcher.py`
### ⚡ `**JarvisLauncher**.__init__(self, root)`
- *Dòng:* 14

### ⚡ `**JarvisLauncher**.launch_main_cmd(self, cmd_args)`
- *Mô tả:* Chạy main.py thông qua subprocess với tham số.
- *Dòng:* 82

### ⚡ `**JarvisLauncher**.log(self, message)`
- *Mô tả:* Ghi thông tin vào cửa sổ Log.
- *Dòng:* 77

### ⚡ `**JarvisLauncher**.run_process(self, cmd_list)`
- *Mô tả:* Thực thi tiến trình và bắt log realtime.
- *Dòng:* 94

### ⚡ `**JarvisLauncher**.setup_ui(self)`
- *Mô tả:* Thiết lập giao diện tích hợp với main.py.
- *Dòng:* 22

## 📁 `projects\jarvis-rpg-assistant\src\note.py`
### ⚡ `main(args)`
- *Mô tả:* Điểm vào CLI để ghi chú nhanh.
- *Dòng:* 19

## 📁 `projects\jarvis-rpg-assistant\src\note_search.py`
### ⚡ `main()`
- *Dòng:* 78

### ⚡ `read_journal()`
- *Mô tả:* Đọc toàn bộ nội dung file ghi chú.
- *Dòng:* 19

### ⚡ `search_in_notes(query)`
- *Mô tả:* Gửi nội dung ghi chú + câu hỏi cho AI xử lý.
- *Dòng:* 36

## 📁 `projects\jarvis-rpg-assistant\src\test_vision_calendar.py`
### ⚡ `get_next_weekday(day_name)`
- *Mô tả:* Hàm tính toán ngày tháng (YYYY-MM-DD) cho ngày trong tuần gần nhất. Ví dụ: 'Thứ 2' -> trả về YYYY-MM-DD của thứ 2 tuần này/tuần tới.
- *Dòng:* 12

### ⚡ `test_pipeline(image_path)`
- *Dòng:* 43

## 📁 `projects\jarvis-rpg-assistant\tests\conftest.py`
### ⚡ `pytest_configure(config)`
- *Dòng:* 3

## 📁 `projects\jarvis-rpg-assistant\tests\test_ai_agent.py`
### ⚡ `**TestAIService**.ai_service(self, mock_key_manager)`
- *Mô tả:* Create AI service with mocked dependencies
- *Dòng:* 21

### ⚡ `**TestAIService**.mock_key_manager(self)`
- *Mô tả:* Mock key manager
- *Dòng:* 14

### ⚡ `**TestAIService**.test_cache_functionality(self, ai_service)`
- *Mô tả:* Test caching mechanism
- *Dòng:* 33

### ⚡ `**TestAIService**.test_cache_ttl_configuration(self, ai_service)`
- *Mô tả:* Test cache TTL configuration
- *Dòng:* 68

### ⚡ `**TestAIService**.test_generate_content_with_retry(self, mock_model, ai_service)`
- *Mô tả:* Test generate content with retry mechanism
- *Dòng:* 39

### ⚡ `**TestAIService**.test_init_ai_service(self, ai_service)`
- *Mô tả:* Test AI service initialization
- *Dòng:* 27

### ⚡ `**TestAIService**.test_key_manager_integration(self, ai_service, mock_key_manager)`
- *Mô tả:* Test integration with key manager
- *Dòng:* 57

### ⚡ `**TestAIService**.test_model_priority_list(self, ai_service)`
- *Mô tả:* Test that model priority is defined
- *Dòng:* 61

## 📁 `projects\jarvis-rpg-assistant\tests\test_core.py`
### ⚡ `key_manager()`
- *Mô tả:* Create a key manager instance for testing
- *Dòng:* 27

### ⚡ `temp_db()`
- *Mô tả:* Create a temporary database for testing
- *Dòng:* 13

### ⚡ `**TestDatabaseManager**.test_add_vocab(self, temp_db)`
- *Mô tả:* Test adding vocabulary
- *Dòng:* 66

### ⚡ `**TestDatabaseManager**.test_database_close(self, temp_db)`
- *Mô tả:* Test database cleanup
- *Dòng:* 118

### ⚡ `**TestDatabaseManager**.test_get_due_vocab(self, temp_db)`
- *Mô tả:* Test getting due vocabulary
- *Dòng:* 76

### ⚡ `**TestKeyManager**.test_get_next_key(self, key_manager)`
- *Mô tả:* Test getting next available key
- *Dòng:* 130

### ⚡ `**TestKeyManager**.test_get_next_key_rotation(self, key_manager)`
- *Mô tả:* Test key rotation
- *Dòng:* 135

### ⚡ `**TestDatabaseManager**.test_get_review_candidates_new(self, temp_db)`
- *Mô tả:* Test getting new vocabulary for review
- *Dòng:* 86

### ⚡ `**TestDatabaseManager**.test_get_review_candidates_review(self, temp_db)`
- *Mô tả:* Test getting vocabulary for review
- *Dòng:* 95

### ⚡ `**TestDatabaseManager**.test_get_user_profile(self, temp_db)`
- *Mô tả:* Test getting user profile
- *Dòng:* 44

### ⚡ `**TestDatabaseManager**.test_init_creates_tables(self, temp_db)`
- *Mô tả:* Test that database initialization creates all required tables
- *Dòng:* 33

### ⚡ `**TestKeyManager**.test_init_key_manager(self, key_manager)`
- *Mô tả:* Test key manager initialization
- *Dòng:* 125

### ⚡ `**TestKeyManager**.test_mark_key_exhausted(self, key_manager)`
- *Mô tả:* Test marking key as exhausted
- *Dòng:* 144

### ⚡ `**TestKeyManager**.test_reset_exhausted_keys(self, key_manager)`
- *Mô tả:* Test resetting exhausted keys
- *Dòng:* 160

### ⚡ `**TestDatabaseManager**.test_update_user_stats(self, temp_db)`
- *Mô tả:* Test updating user stats
- *Dòng:* 55

### ⚡ `**TestDatabaseManager**.test_update_vocab_mastery_correct(self, temp_db)`
- *Mô tả:* Test updating vocabulary when remembered correctly
- *Dòng:* 104

### ⚡ `**TestDatabaseManager**.test_update_vocab_mastery_incorrect(self, temp_db)`
- *Mô tả:* Test updating vocabulary when not remembered
- *Dòng:* 111

## 📁 `projects\jarvis-rpg-assistant\tests\test_new_features.py`
### ⚡ `**TestConfigModule**.test_config_module_imports(self)`
- *Mô tả:* Test that config module can be imported
- *Dòng:* 8

### ⚡ `**TestConfigModule**.test_config_paths_exist(self)`
- *Mô tả:* Test that config defines required paths
- *Dòng:* 16

### ⚡ `**TestKeyManager**.test_key_manager_basic(self)`
- *Mô tả:* Test key manager basic functionality
- *Dòng:* 27

### ⚡ `**TestKeyManager**.test_key_rotation(self)`
- *Mô tả:* Test key rotation mechanism
- *Dòng:* 36

## 📁 `projects\jarvis-rpg-assistant\tools\admin_gui.py`
### ⚡ `**JarvisAdminApp**.__init__(self, root)`
- *Dòng:* 13

### ⚡ `**JarvisAdminApp**.add_word(self)`
- *Dòng:* 136

### ⚡ `**JarvisAdminApp**.delete_word(self)`
- *Dòng:* 176

### ⚡ `**JarvisAdminApp**.hack_time(self)`
- *Dòng:* 193

### ⚡ `**JarvisAdminApp**.load_data(self)`
- *Dòng:* 110

### ⚡ `**JarvisAdminApp**.on_select(self, event)`
- *Dòng:* 125

### ⚡ `**JarvisAdminApp**.run_query(self, query, params)`
- *Dòng:* 91

### ⚡ `**JarvisAdminApp**.update_word(self)`
- *Dòng:* 158

## 📁 `projects\jarvis-rpg-assistant\tools\bot_sync.py`
### ⚡ `**ScheduleSyncApp**.__init__(self, root)`
- *Dòng:* 38

### ⚡ `**ScheduleSyncApp**.handle_drop(self, event)`
- *Dòng:* 108

### ⚡ `**ScheduleSyncApp**.log(self, message)`
- *Dòng:* 85

### ⚡ `**ScheduleSyncApp**.process_with_ai(self, input_data, is_image)`
- *Dòng:* 176

### ⚡ `**ScheduleSyncApp**.push_to_google_calendar(self, events_json)`
- *Dòng:* 217

### ⚡ `**ScheduleSyncApp**.run_process_images(self, file_paths)`
- *Dòng:* 161

### ⚡ `**ScheduleSyncApp**.run_web_sync(self)`
- *Dòng:* 126

### ⚡ `**ScheduleSyncApp**.start_img_sync_thread(self, file_paths)`
- *Dòng:* 95

### ⚡ `**ScheduleSyncApp**.start_web_sync_thread(self)`
- *Dòng:* 92

## 📁 `projects\jarvis-rpg-assistant\tools\calendar_ui.py`
### ⚡ `generate_google_calendar_csv(events)`
- *Mô tả:* Tạo nội dung CSV chuẩn Google Calendar.
- *Dòng:* 35

### ⚡ `get_next_weekday(day_name)`
- *Mô tả:* Tính ngày tháng (YYYY-MM-DD) cho ngày trong tuần gần nhất.
- *Dòng:* 16

## 📁 `projects\jarvis-rpg-assistant\tools\cheat_db.py`
### ⚡ `hack_time()`
- *Dòng:* 10

## 📁 `projects\jarvis-rpg-assistant\tools\dashboard.py`
### ⚡ `get_db()`
- *Dòng:* 27

## 📁 `projects\jarvis-rpg-assistant\tools\public_readiness_check.py`
### ⚡ `run_command(cmd, ignore_warning)`
- *Dòng:* 9

## 📁 `projects\jarvis-rpg-assistant\tools\test_key.py`
### ⚡ `load_keys_from_file(file_path)`
- *Mô tả:* Đọc tất cả API Key từ file, loại bỏ khoảng trắng và dòng trống.
- *Dòng:* 8

### ⚡ `quick_verify_api(api_key)`
- *Mô tả:* Hàm kiểm tra nhanh 1 key
- *Dòng:* 19

## 📁 `projects\knowledge_base_agent\src\ingest.py`
### ⚡ `bootstrap_environment()`
- *Mô tả:* Khởi tạo toàn bộ hạ tầng thư mục lưu trữ nếu chưa tồn tại.
- *Dòng:* 28

### ⚡ `collect_pending_assets(target_dir)`
- *Mô tả:* Quét và thu thập danh sách các tập tin PDF đang chờ xử lý.
- *Dòng:* 34

### ⚡ `commit_to_vectorstore(chunks, embeddings, db_path)`
- *Mô tả:* Lưu trữ các vector dữ liệu vào hệ quản trị cơ sở dữ liệu vector ChromaDB.
- *Dòng:* 90

### ⚡ `parse_pdf_to_markdown_and_chunk(pdf_files, chunk_size, chunk_overlap)`
- *Mô tả:* Trích xuất PDF bằng PyMuPDF4LLM, băm theo Markdown và Recursive.
- *Dòng:* 39

### ⚡ `relocate_processed_assets(source_files, destination_dir)`
- *Mô tả:* Di chuyển các tệp tin gốc đã xử lý thành công sang phân vùng lưu trữ lâu dài.
- *Dòng:* 105

### ⚡ `run_pipeline()`
- *Mô tả:* Hàm điều phối (Orchestrator) thực thi toàn bộ chu trình nạp dữ liệu.
- *Dòng:* 119

### ⚡ `safe_initialize_embeddings()`
- *Mô tả:* Khởi tạo mô hình Embedding cục bộ. Tích hợp cơ chế Fallback.
- *Dòng:* 76

## 📁 `projects\knowledge_base_agent\src\rag_agent.py`
### ⚡ `**RAGAgent**.__init__(self, model_name)`
- *Dòng:* 23

### ⚡ `**RAGAgent**._ai_handler(self, state)`
- *Dòng:* 70

### ⚡ `**RAGAgent**._logic_handler(self, state)`
- *Dòng:* 73

### ⚡ `**RAGAgent**.query(self, question)`
- *Mô tả:* Nhận câu hỏi, tìm kiếm relevant chunks và đưa cho LLM tổng hợp câu trả lời.
- *Dòng:* 40

## 📁 `projects\local_proxy_server\core\adapter.py`
### ⚡ `_extract_next_json_object(buffer)`
- *Mô tả:* Find the first complete top-level JSON object in buffer using brace-depth.  Returns:     Tuple of (object_string, remainder) or (None, buffer) if inco...
- *Dòng:* 261

### ⚡ `_extract_text_from_gemini_obj(obj)`
- *Mô tả:* Extract output text from a single parsed Gemini stream object, skipping any thought tokens (Gemini 3.x / Gemma-4 reasoning).
- *Dòng:* 167

### ⚡ `_trim_messages_if_needed(messages)`
- *Mô tả:* Tiêu chuẩn 1: Zero Token Leakage. Đo độ dài payload bằng thuật toán cơ bản (tương đương tiktoken),  nếu quá dài thì tự động cắt tỉa các tin nhắn cũ nh...
- *Dòng:* 12

### ⚡ `async stream_gemini_to_openai(gemini_stream)`
- *Mô tả:* Transform Gemini streaming response to OpenAI SSE format.  Robust brace-depth parser: accumulates bytes into a buffer, finds complete JSON objects by ...
- *Dòng:* 188

### ⚡ `to_gemini_payload(openai_payload)`
- *Mô tả:* Convert OpenAI-compatible chat completion payload to Gemini API format.  Args:     openai_payload: Dictionary containing OpenAI format request with 'm...
- *Dòng:* 49

### ⚡ `to_openai_final_chunk()`
- *Mô tả:* Create a final chunk to signal stream completion.  Returns:     SSE formatted string with finish_reason set to 'stop'.
- *Dòng:* 143

### ⚡ `to_openai_stream(gemini_chunk)`
- *Mô tả:*     Convert Gemini streaming response chunk to OpenAI SSE format.          Args:         gemini_chunk: Raw text chunk from Gemini streaming response. ...
- *Dòng:* 108

## 📁 `projects\local_proxy_server\core\config.py`
### ⚡ `**Settings**.__init__(self)`
- *Mô tả:* Initialize settings and validate required environment variables.
- *Dòng:* 24

### ⚡ `**Settings**.get_gemini_stream_url(self, model_name, api_key)`
- *Mô tả:* Build the Gemini streaming endpoint URL for a specific (model, key) pair.  Args:     model_name: The exact target model name (already mapped).     api...
- *Dòng:* 163

### ⚡ `get_settings()`
- *Mô tả:* Get the global settings instance.  Returns:     Settings: The application settings instance.  Raises:     ValueError: If GEMINI_API_KEY is not configu...
- *Dòng:* 188

### ⚡ `**Settings**.map_model(self, requested_model)`
- *Mô tả:* Map requested model name or label to actual Google API model string.
- *Dòng:* 149

## 📁 `projects\local_proxy_server\core\rotation_manager.py`
### ⚡ `**RotationManager**.__init__(self)`
- *Dòng:* 19

### ⚡ `**RotationManager**._is_exhausted(self, key, model)`
- *Dòng:* 32

### ⚡ `**RotationManager**._maybe_auto_reset(self)`
- *Mô tả:* Auto-reset pool when the calendar day changes (UTC).
- *Dòng:* 135

### ⚡ `get_rotation_manager()`
- *Mô tả:* Get the global RotationManager singleton.
- *Dòng:* 170

### ⚡ `**RotationManager**.get_stats(self)`
- *Mô tả:* Return current rotation statistics for monitoring.
- *Dòng:* 146

### ⚡ `**RotationManager**.get_valid_credential(self, requested_model)`
- *Mô tả:* Find a valid (Key, Model) pair that still has quota.  If the requested model has exhausted all its keys, automatically fall back to other models in th...
- *Dòng:* 59

### ⚡ `**RotationManager**.mark_exhausted(self, key, model)`
- *Mô tả:* Mark a (key, model) pair as quota-exhausted so it is skipped in subsequent dispatches. Also advances the model's key index. Applies Exponential Backof...
- *Dòng:* 106

### ⚡ `**RotationManager**.reset_quota_pool(self)`
- *Mô tả:* Clear all exhausted records. Call at UTC midnight or manually.
- *Dòng:* 129

## 📁 `projects\local_proxy_server\core\router.py`
### ⚡ `_init_billing_db()`
- *Dòng:* 362

### ⚡ `async chat_completions(request)`
- *Mô tả:* OpenAI-compatible chat completions endpoint with streaming support.  This endpoint accepts OpenAI-format requests and proxies them to Gemini API, tran...
- *Dòng:* 238

### ⚡ `async health_check()`
- *Mô tả:* Health check endpoint.  Returns:     Dictionary with health status.
- *Dòng:* 348

### ⚡ `async process_billing(request)`
- *Mô tả:* Tiêu chuẩn 3: Crypto Payment Config Ready & Anti-Replay Endpoint nhận TxHash, kiểm tra trùng lặp và lưu vào billing.db
- *Dòng:* 389

### ⚡ `async root()`
- *Mô tả:* Root endpoint with service information.  Returns:     Dictionary with service information.
- *Dòng:* 443

### ⚡ `async stream_fallback_generator(openai_payload, requested_model)`
- *Mô tả:* Fallback generator using Groq or OpenRouter when Gemini is fully exhausted.
- *Dòng:* 22

### ⚡ `async stream_generator(gemini_payload, requested_model, openai_payload)`
- *Mô tả:* Async generator that streams responses from Gemini and converts to OpenAI format. Uses RotationManager for smart (key, model) dispatch with automatic ...
- *Dòng:* 113

## 📁 `projects\local_proxy_server\tests\test_proxy.py`
### ⚡ `make_manager(num_keys)`
- *Mô tả:* Build a RotationManager with a fake Settings containing N keys.
- *Dòng:* 22

### ⚡ `test_basic_dispatch()`
- *Mô tả:* Test 1: Basic credential dispatch returns a valid pair.
- *Dòng:* 46

### ⚡ `test_fallback_to_alternative_model()`
- *Mô tả:* Test 3: When all keys of requested model die, fallback to alternative model.
- *Dòng:* 71

### ⚡ `test_full_exhaustion()`
- *Mô tả:* Test 4: All pairs exhausted -> RuntimeError.
- *Dòng:* 90

### ⚡ `test_mark_exhausted_skip()`
- *Mô tả:* Test 2: Marked pair is skipped on next dispatch.
- *Dòng:* 57

### ⚡ `test_stats()`
- *Mô tả:* Test 5: get_stats returns accurate counts.
- *Dòng:* 111

## 📁 `projects\local_proxy_server\tests\test_proxy_server.py`
### ⚡ `run_tests()`
- *Mô tả:* Run all tests.
- *Dòng:* 206

### ⚡ `test_adapter_to_gemini_payload()`
- *Mô tả:* Test conversion from OpenAI to Gemini payload format.
- *Dòng:* 18

### ⚡ `test_adapter_to_openai_stream()`
- *Mô tả:* Test conversion from Gemini chunk to OpenAI SSE format.
- *Dòng:* 56

### ⚡ `test_api_key_rotation_logic()`
- *Mô tả:* Test the configuration loading and rotation mechanism of API Keys.
- *Dòng:* 86

### ⚡ `async test_chat_completions_stream()`
- *Mô tả:* Test the chat completions endpoint with streaming.
- *Dòng:* 147

### ⚡ `async test_health_endpoint()`
- *Mô tả:* Test the health check endpoint.
- *Dòng:* 120

### ⚡ `async test_root_endpoint()`
- *Mô tả:* Test the root endpoint.
- *Dòng:* 133

## 📁 `projects\qa_chaos_agent\src\encyclopedia_writer.py`
### ⚡ `write_to_encyclopedia(error_name, symptoms, root_cause, action_item)`
- *Mô tả:* Ghi lỗi mới vào Bách khoa toàn thư để các Agent RAG có thể học được.
- *Dòng:* 5

## 📁 `projects\qa_chaos_agent\src\fuzzer_engine.py`
### ⚡ `**FuzzerEngine**.__init__(self)`
- *Dòng:* 17

### ⚡ `**FuzzerEngine**.dummy_fuzz_import(self, file_path)`
- *Mô tả:* Thử import module động để kiểm tra lỗi cú pháp, lỗi thiếu import (ModuleNotFoundError), hoặc code chạy ngoài scope.
- *Dòng:* 36

### ⚡ `**FuzzerEngine**.extract_python_files_from_map(self)`
- *Mô tả:* Đọc SYSTEM_MAP.md để lấy ra các file Python có thể Fuzz.
- *Dòng:* 21

### ⚡ `**FuzzerEngine**.process_crash(self, module_name, tb)`
- *Dòng:* 60

### ⚡ `**FuzzerEngine**.run_nightly_fuzz(self, max_files)`
- *Mô tả:* Chạy Fuzzing ngẫu nhiên 2 file mỗi đêm để nhẹ server.
- *Dòng:* 72

## 📁 `projects\qa_chaos_agent\src\llm_autopsy.py`
### ⚡ `**LLMAutopsy**.__init__(self)`
- *Dòng:* 5

### ⚡ `**LLMAutopsy**._ai_handler(self, state)`
- *Dòng:* 9

### ⚡ `**LLMAutopsy**._logic_handler(self, state)`
- *Dòng:* 12

### ⚡ `**LLMAutopsy**.analyze_crash(self, target_module, traceback_str)`
- *Mô tả:* Gửi Traceback cho LLM phân tích nguyên nhân và cách sửa. Tránh đốt token, chỉ lấy đúng trọng tâm.
- *Dòng:* 15

## 📁 `projects\qa_functional_agent\src\functional_tester.py`
### ⚡ `**FunctionalTester**.__init__(self)`
- *Dòng:* 13

### ⚡ `**FunctionalTester**._ai_handler(self, state)`
- *Dòng:* 16

### ⚡ `**FunctionalTester**._logic_handler(self, state)`
- *Dòng:* 19

### ⚡ `**FunctionalTester**.ai_assert(self, expected_behavior, actual_output)`
- *Mô tả:* Sử dụng LLM để chấm điểm kết quả (Functional Assertion).
- *Dòng:* 22

### ⚡ `**FunctionalTester**.test_script_generator(self)`
- *Mô tả:* Unit/Functional test cho ScriptGenerator của Auto Affiliate Video
- *Dòng:* 101

### ⚡ `**FunctionalTester**.test_streamlit_ui(self)`
- *Mô tả:* Dùng Playwright test Streamlit UI (End-to-End)
- *Dòng:* 47

## 📁 `projects\sillytavern_world_card_generator\src\auto_translator.py`
### ⚡ `**AutoTranslatorAgent**.__init__(self)`
- *Dòng:* 29

### ⚡ `batch_translate(input_dir, output_dir, limit)`
- *Dòng:* 83

### ⚡ `translate_card(input_file, output_file)`
- *Dòng:* 48

### ⚡ `**AutoTranslatorAgent**.translate_text(self, text)`
- *Dòng:* 33

## 📁 `projects\sillytavern_world_card_generator\src\ingest_cards.py`
### ⚡ `extract_card_text(json_data)`
- *Mô tả:* Trích xuất các trường nội dung quan trọng từ thẻ JSON của SillyTavern.
- *Dòng:* 20

### ⚡ `ingest_cards()`
- *Dòng:* 56

## 📁 `projects\sillytavern_world_card_generator\src\lore_extractor.py`
### ⚡ `async agent_process_card(filepath)`
- *Dòng:* 165

### ⚡ `build_llm_prompt(data)`
- *Dòng:* 45

### ⚡ `async call_llm_api(messages)`
- *Dòng:* 110

### ⚡ `get_output_filename(md_content, original_name)`
- *Dòng:* 142

### ⚡ `get_processed_files()`
- *Dòng:* 155

### ⚡ `has_chinese_chars(text)`
- *Dòng:* 152

### ⚡ `log_processed_file(filename)`
- *Dòng:* 161

### ⚡ `async main()`
- *Dòng:* 181

### ⚡ `read_json_file(filepath)`
- *Dòng:* 38

### ⚡ `write_markdown_file(filepath, content, original_name)`
- *Dòng:* 133

## 📁 `projects\sillytavern_world_card_generator\src\world_card_generator.py`
### ⚡ `**WorldCardGenerator**.__init__(self)`
- *Dòng:* 13

### ⚡ `**WorldCardGenerator**.export_to_json(self, card, filename)`
- *Mô tả:* Xuất file JSON.
- *Dòng:* 78

### ⚡ `**WorldCardGenerator**.generate(self, user_idea)`
- *Mô tả:* Chạy quy trình sinh dữ liệu bằng AI thực.
- *Dòng:* 18

## 📁 `projects\sillytavern_world_card_generator\tests\test_basic.py`
### ⚡ `test_basic_initialization()`
- *Mô tả:* Basic test to ensure project initializes correctly.
- *Dòng:* 2

## 📁 `projects\sillytavern_world_card_generator\tools\non_ai_lorebook_extractor.py`
### ⚡ `**LorebookExtractor**.__init__(self, use_spacy)`
- *Dòng:* 17

### ⚡ `**LorebookExtractor**._extract_characters_regex(self, text)`
- *Dòng:* 44

### ⚡ `**LorebookExtractor**.analyze_traits(self, context_text)`
- *Mô tả:* Analyzes context text against keyword dictionaries.
- *Dòng:* 74

### ⚡ `**LorebookExtractor**.create_sillytavern_entry(self, uid, name, traits)`
- *Mô tả:* Formats the extracted traits into a SillyTavern JSON entry.
- *Dòng:* 99

### ⚡ `**LorebookExtractor**.extract_context_around_name(self, text, name, window)`
- *Mô tả:* Extracts context around mentions of a character.
- *Dòng:* 59

### ⚡ `**LorebookExtractor**.process_file(self, input_path, output_path)`
- *Dòng:* 140

## 📁 `projects\sillytavern_world_card_generator\tools\streamlit_lorebook_app.py`
### ⚡ `**OllamaLorebookExtractor**.__init__(self, api_url)`
- *Dòng:* 9

### ⚡ `**OllamaLorebookExtractor**.extract_with_ai(self, text, model_name, char_name)`
- *Mô tả:* Sends text to Ollama and expects a JSON response formatted for SillyTavern.
- *Dòng:* 23

### ⚡ `**OllamaLorebookExtractor**.get_available_models(self)`
- *Mô tả:* Fetches available models from the Ollama instance.
- *Dòng:* 12

## 📁 `projects\sovereign_terminal\core\config.py`
### ⚡ `**Config**.get_client_config(cls)`
- *Mô tả:* Trả về config cho OpenAI client.
- *Dòng:* 49

### ⚡ `**Config**.validate(cls)`
- *Mô tả:* Kiểm tra xem API Key đã được cấu hình chưa.
- *Dòng:* 40

## 📁 `projects\sovereign_terminal\core\mcp_client.py`
### ⚡ `**MCPManager**.__init__(self)`
- *Dòng:* 17

### ⚡ `async **MCPManager**.close(self)`
- *Dòng:* 109

### ⚡ `async **MCPManager**.connect_all(self)`
- *Dòng:* 32

### ⚡ `async **MCPManager**.execute_tool(self, tool_name, arguments)`
- *Dòng:* 85

### ⚡ `**MCPManager**.load_config(self, config_path)`
- *Dòng:* 24

## 📁 `projects\sovereign_terminal\core\persona.py`
### ⚡ `load_persona()`
- *Mô tả:* Load System Prompt đồ sộ từ các file cốt lõi của hệ thống. Giúp Agent có 100% trí nhớ và tính cách của CEO Sovereign.
- *Dòng:* 9

## 📁 `projects\sovereign_terminal\core\tools.py`
### ⚡ `execute_tool(name, arguments)`
- *Mô tả:* Thực thi tool theo tên và trả về kết quả.
- *Dòng:* 211

### ⚡ `list_files(path, recursive)`
- *Mô tả:* Liệt kê files trong thư mục.
- *Dòng:* 74

### ⚡ `read_file(path)`
- *Mô tả:* Đọc nội dung file.
- *Dòng:* 11

### ⚡ `run_command(command)`
- *Mô tả:* Chạy lệnh terminal.
- *Dòng:* 42

### ⚡ `trigger_factory_workflow(mode, project_name, requirement)`
- *Mô tả:* Kích hoạt LangGraph Factory Workflow (DevOps từ xa).
- *Dòng:* 99

### ⚡ `write_file(path, content)`
- *Mô tả:* Ghi nội dung vào file.
- *Dòng:* 26

## 📁 `projects\sovereign_terminal\gateways\telegram_bot.py`
### ⚡ `async handle_text(update, context)`
- *Dòng:* 97

### ⚡ `async initialize_system()`
- *Dòng:* 27

### ⚡ `async process_message(user_message, chat_id)`
- *Dòng:* 45

### ⚡ `async reset_cmd(update, context)`
- *Dòng:* 92

### ⚡ `async run_bot()`
- *Dòng:* 116

### ⚡ `async start_cmd(update, context)`
- *Dòng:* 89

## 📁 `projects\universal_game_vault\src\scraper.py`
### ⚡ `**GameWebScraper**.__init__(self)`
- *Dòng:* 21

### ⚡ `**GameWebScraper**._ai_handler(self)`
- *Dòng:* 27

### ⚡ `**GameWebScraper**._logic_handler(self)`
- *Dòng:* 30

### ⚡ `**GameWebScraper**.scrape_url(self, url)`
- *Mô tả:* Cào nội dung văn bản từ một URL.
- *Dòng:* 33

## 📁 `projects\universal_web_scraper\src\alonhadat_parser.py`
### ⚡ `**BaseScraper**.__init__(self, log_file, raw_data_path)`
- *Dòng:* 13

### ⚡ `**AlonhadatParser**.__init__(self, log_file, raw_data_path, output_csv)`
- *Dòng:* 82

### ⚡ `**BaseScraper**.add_scraped_page(self, page)`
- *Mô tả:* Ghi nhận một trang đã cào thành công.
- *Dòng:* 29

### ⚡ `**AlonhadatParser**.build_headers(self)`
- *Dòng:* 87

### ⚡ `**BaseScraper**.clean_old_data(self)`
- *Mô tả:* Xóa dữ liệu rác (Area < 10, District chứa tên đường) khỏi file gộp.
- *Dòng:* 34

### ⚡ `**BaseScraper**.get_scraped_pages(self)`
- *Mô tả:* Đọc danh sách các trang đã cào thành công từ log file.
- *Dòng:* 21

### ⚡ `**BaseScraper**.incremental_merge(self, new_data, output_csv)`
- *Mô tả:* Gộp dữ liệu mới vào output_csv nội bộ và raw_data.csv của mô hình.
- *Dòng:* 43

### ⚡ `**AlonhadatParser**.run_guerrilla(self, max_pages, batch_size)`
- *Mô tả:* Chiến thuật Cào Du Kích: Trộn trang, cào từng batch nhỏ rồi nghỉ.
- *Dòng:* 189

### ⚡ `**AlonhadatParser**.scrape_page(self, page)`
- *Dòng:* 107

## 📁 `projects\universal_web_scraper\src\alonhadat_playwright.py`
### ⚡ `**AlonhadatPlaywrightScraper**.__init__(self, output_csv, raw_data_path)`
- *Dòng:* 17

### ⚡ `**AlonhadatPlaywrightScraper**.parse_page_data(self, page)`
- *Dòng:* 22

### ⚡ `**AlonhadatPlaywrightScraper**.run_scraper(self, target_pages)`
- *Dòng:* 99

### ⚡ `**AlonhadatPlaywrightScraper**.save_and_merge(self, data)`
- *Dòng:* 143

## 📁 `projects\universal_web_scraper\src\base_scraper.py`
### ⚡ `**PlaywrightStealth**.human_pause(min_sec, max_sec)`
- *Dòng:* 18

### ⚡ `**PlaywrightStealth**.random_scroll(page, min_scrolls, max_scrolls)`
- *Dòng:* 6

## 📁 `projects\universal_web_scraper\src\batdongsan_playwright.py`
### ⚡ `**BatDongSanPlaywrightScraper**.__init__(self, output_csv, raw_data_db)`
- *Dòng:* 22

### ⚡ `**BatDongSanPlaywrightScraper**.add_scraped_page(self, page)`
- *Dòng:* 35

### ⚡ `**BatDongSanPlaywrightScraper**.get_scraped_pages(self)`
- *Dòng:* 27

### ⚡ `**BatDongSanPlaywrightScraper**.parse_page_data(self, page)`
- *Dòng:* 40

### ⚡ `**BatDongSanPlaywrightScraper**.run_guerrilla(self, max_pages, batch_size)`
- *Dòng:* 121

### ⚡ `**BatDongSanPlaywrightScraper**.save_and_merge(self, data)`
- *Dòng:* 188

## 📁 `projects\universal_web_scraper\src\cleaner.py`
### ⚡ `clean_and_rank_data(input_csv, output_csv)`
- *Mô tả:* Làm sạch dữ liệu Hacker News, tính Engagement_Score và lưu kết quả.  Args:     input_csv (str): Đường dẫn tới file CSV thô (hn_results.csv).     outpu...
- *Dòng:* 5

## 📁 `projects\universal_web_scraper\src\parser.py`
### ⚡ `parse_hacker_news(html_path, output_csv)`
- *Mô tả:* Parse Hacker News HTML and extract title, href, score, and comments.  Args:     html_path (str): Path to the raw HTML file.     output_csv (str): Path...
- *Dòng:* 6

## 📁 `sillytavern_world_card_generator\src\agents\base_agent.py`
### ⚡ `**BaseGeminiAgent**.__init__(self, model_name, temperature)`
- *Dòng:* 16

### ⚡ `**BaseGeminiAgent**._ai_handler(self)`
- *Dòng:* 25

### ⚡ `**BaseGeminiAgent**._call_gemini(self, prompt, is_json)`
- *Mô tả:* Gửi prompt đến LLM sử dụng hệ thống gọi API đã chuẩn hóa. Hàm này vẫn trả về chuỗi JSON thô (string) để tương thích ngược với code cũ, nhưng thực tế n...
- *Dòng:* 31

### ⚡ `**BaseGeminiAgent**._logic_handler(self)`
- *Dòng:* 28

### ⚡ `**BaseGeminiAgent**._parse_json_response(self, response_text)`
- *Mô tả:* Sử dụng logic parse chuẩn từ BaseAgent.
- *Dòng:* 51

## 📁 `sillytavern_world_card_generator\src\agents\coder_agent.py`
### ⚡ `**CoderAgent**.__init__(self, model_name)`
- *Dòng:* 40

### ⚡ `generate_code_mock(user_idea)`
- *Dòng:* 149

### ⚡ `**CoderAgent**.generate_extensions(self, user_idea)`
- *Mô tả:* Sinh ra các file extension dựa trên tính năng được yêu cầu.
- *Dòng:* 43

## 📁 `sillytavern_world_card_generator\src\agents\lore_master_agent.py`
### ⚡ `**LoreMasterAgent**.__init__(self, model_name)`
- *Dòng:* 52

### ⚡ `generate_lore_mock(user_idea)`
- *Dòng:* 152

### ⚡ `**LoreMasterAgent**.generate_lorebook(self, user_idea)`
- *Mô tả:* Tạo danh sách Lorebook entries bằng Gemini. Hỗ trợ RAG (đọc file mẫu) và Auto-balancing.
- *Dòng:* 56

## 📁 `sillytavern_world_card_generator\src\agents\rag_card_agent.py`
### ⚡ `**RAGCardAgent**.__init__(self)`
- *Dòng:* 15

### ⚡ `**RAGCardAgent**.get_reference_context(self, theme, style)`
- *Mô tả:* Lấy context từ các thẻ cũ dựa trên theme và style.
- *Dòng:* 30

## 📁 `sillytavern_world_card_generator\src\agents\storyteller_agent.py`
### ⚡ `**StorytellerAgent**.__init__(self, model_name)`
- *Dòng:* 40

### ⚡ `**StorytellerAgent**.generate_narrative_context(self, user_idea)`
- *Mô tả:* Tạo System Prompt và First Message từ ý tưởng người dùng bằng Gemini.
- *Dòng:* 44

## 📁 `sillytavern_world_card_generator\src\models\world_card_v3.py`
### ⚡ `**WorldCardV3**.to_json(self)`
- *Mô tả:* Xuất ra chuỗi JSON đẹp mắt.
- *Dòng:* 122

## 📁 `src\factory\nodes\architecture_critic.py`
### ⚡ `**ArchitectureCritic**.__init__(self)`
- *Dòng:* 13

### ⚡ `**ArchitectureCritic**._ai_handler(self)`
- *Dòng:* 22

### ⚡ `**ArchitectureCritic**._logic_handler(self)`
- *Dòng:* 42

### ⚡ `architecture_critic_node(state)`
- *Dòng:* 46

## 📁 `src\factory\nodes\coder.py`
### ⚡ `async coder_node(state)`
- *Dòng:* 7

## 📁 `src\factory\nodes\context_manager.py`
### ⚡ `context_manager_node(state)`
- *Mô tả:* Just-In-Time Context Manager. Dựa vào route đã được Semantic Router chọn, bơm đúng lượng data cần thiết vào State.
- *Dòng:* 13

## 📁 `src\factory\nodes\memory_manager.py`
### ⚡ `memory_manager_node(state)`
- *Dòng:* 15

### ⚡ `truncate_text(text, max_lines)`
- *Dòng:* 9

## 📁 `src\factory\nodes\omni_overlord.py`
### ⚡ `**OmniOverlord**.__init__(self)`
- *Dòng:* 30

### ⚡ `**OmniOverlord**._ai_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 38

### ⚡ `**OmniOverlord**._logic_handler(self)`
- *Mô tả:* Bắt buộc triển khai từ BaseAgent.
- *Dòng:* 42

### ⚡ `**OmniOverlord**.check_market_pulse(self)`
- *Mô tả:* Đọc tin tức và phân tích xem có biến cố khẩn cấp (Emergency) không. Trả về dictionary chứa các trigger flag.
- *Dòng:* 46

## 📁 `src\factory\nodes\patch_generator.py`
### ⚡ `git_patch_node(state)`
- *Mô tả:* Node tạo file .patch dựa trên Draft Code đã được sửa (và pass qua Sandbox). Giả lập việc tạo patch dựa trên diff cơ bản (để tiện lợi không cần commit ...
- *Dòng:* 4

## 📁 `src\factory\nodes\principles_gate.py`
### ⚡ `principles_gate_node(state)`
- *Mô tả:* Sovereign Principles Gate. Đảm bảo mọi yêu cầu và ngữ cảnh đều tuân thủ nguyên lý hệ thống trước khi rẽ nhánh. Tích hợp Self-Healing Loop và Luồng Dra...
- *Dòng:* 12

## 📁 `src\factory\nodes\qa_agent.py`
### ⚡ `**QAAgent**.__init__(self)`
- *Dòng:* 21

### ⚡ `**QAAgent**._ai_handler(self)`
- *Dòng:* 28

### ⚡ `**QAAgent**._logic_handler(self)`
- *Dòng:* 25

### ⚡ `qa_node(state)`
- *Dòng:* 55

## 📁 `src\factory\nodes\qa_reviewer.py`
### ⚡ `**QAReviewer**.__init__(self)`
- *Mô tả:* Khởi tạo các mô hình LLM với Load Balancing.
- *Dòng:* 19

### ⚡ `async **QAReviewer**.evaluate(self, project_path, test_results)`
- *Mô tả:* Chạy tuần tự các bước kiểm tra và trả về báo cáo cuối cùng.
- *Dòng:* 27

### ⚡ `extract_score(report)`
- *Mô tả:* Trích xuất điểm số từ báo cáo.
- *Dòng:* 114

### ⚡ `async qa_node(state)`
- *Dòng:* 124

## 📁 `src\factory\nodes\remediation_agent.py`
### ⚡ `**RemediationAgent**.__init__(self)`
- *Dòng:* 17

### ⚡ `**RemediationAgent**._ai_handler(self)`
- *Dòng:* 20

### ⚡ `**RemediationAgent**._logic_handler(self)`
- *Dòng:* 48

### ⚡ `remediation_node(state)`
- *Dòng:* 51

## 📁 `src\factory\nodes\router_agent.py`
### ⚡ `**SemanticRouter**.__init__(self)`
- *Dòng:* 25

### ⚡ `**SemanticRouter**._ai_handler(self)`
- *Dòng:* 65

### ⚡ `**SemanticRouter**._logic_handler(self)`
- *Dòng:* 68

### ⚡ `**SemanticRouter**.route_query(self, query)`
- *Dòng:* 28

### ⚡ `router_node(state)`
- *Dòng:* 71

## 📁 `src\factory\nodes\sandbox_validator.py`
### ⚡ `**SandboxValidator**.__init__(self, workspace_path, timeout)`
- *Dòng:* 19

### ⚡ `async **SandboxValidator**.execute_test_sandbox(self, test_target)`
- *Mô tả:* Thực thi test suite một cách bất đồng bộ bằng lệnh 'uv run pytest'. Tránh nghẽn luồng chính của hệ thống LangGraph.
- *Dòng:* 23

### ⚡ `sandbox_validator_node(state)`
- *Mô tả:* Node LangGraph thực thi kiểm thử.  Lưu ý: Vì Graph chính chạy bất đồng bộ (ainvoke), ta có thể sử dụng asyncio.run (hoặc await nếu đổi node thành asyn...
- *Dòng:* 70

## 📁 `src\factory\nodes\system_designer.py`
### ⚡ `**SystemDesigner**.__init__(self)`
- *Dòng:* 13

### ⚡ `**SystemDesigner**._ai_handler(self, inventory_data)`
- *Dòng:* 22

### ⚡ `**SystemDesigner**._logic_handler(self)`
- *Dòng:* 50

### ⚡ `**SystemDesigner**.generate_mermaid_map(self, inventory_report_path, output_path)`
- *Mô tả:* Đọc báo cáo từ AID Taskforce và sinh biểu đồ Mermaid.
- *Dòng:* 53

## 📁 `src\factory\nodes\triage_director.py`
### ⚡ `async triage_director_node(state)`
- *Dòng:* 28

### ⚡ `async triage_issues_and_plan(qa_report, test_results, llm)`
- *Mô tả:* Technical Director: Phân loại lỗi và lên kế hoạch sửa chữa.
- *Dòng:* 6

## 📁 `src\factory\nodes\workflow_agent.py`
### ⚡ `**AIWorkflowAgent**.__init__(self)`
- *Dòng:* 24

### ⚡ `**AIWorkflowAgent**._ai_handler(self)`
- *Dòng:* 68

### ⚡ `**AIWorkflowAgent**._logic_handler(self)`
- *Dòng:* 71

### ⚡ `**AIWorkflowAgent**.decide_workflow(self, state)`
- *Dòng:* 28

### ⚡ `workflow_agent_node(state)`
- *Dòng:* 75

## 📁 `src\factory\workflows\daily_health_loop.py`
### ⚡ `**ArchitectAgent**.__init__(self)`
- *Dòng:* 17

### ⚡ `**WardenAgent**.__init__(self)`
- *Dòng:* 44

### ⚡ `**ArchitectAgent**._ai_handler(self, health_report)`
- *Dòng:* 20

### ⚡ `**WardenAgent**._ai_handler(self, proposal)`
- *Dòng:* 47

### ⚡ `**ArchitectAgent**._logic_handler(self, health_report)`
- *Dòng:* 40

### ⚡ `**WardenAgent**._logic_handler(self, proposal)`
- *Dòng:* 68

### ⚡ `architect_node(state)`
- *Mô tả:* Analysis & Proposition.
- *Dòng:* 90

### ⚡ `build_daily_health_graph()`
- *Dòng:* 132

### ⚡ `mechanic_node(state)`
- *Mô tả:* Implementation & Patching using AST.
- *Dòng:* 108

### ⚡ `nightwatch_node(state)`
- *Mô tả:* Telemetry & Log Collection.
- *Dòng:* 73

### ⚡ `test_pilot_node(state)`
- *Mô tả:* Benchmark & State Management.
- *Dòng:* 120

### ⚡ `warden_node(state)`
- *Mô tả:* Security & Risk Firewall.
- *Dòng:* 99

## 📁 `src\factory\workflows\software_production.py`
### ⚡ `build_factory_graph()`
- *Mô tả:* Khởi tạo toàn bộ dây chuyền sản xuất phần mềm khép kín.
- *Dòng:* 46

### ⚡ `check_qa_score(state)`
- *Mô tả:* Điều kiện lặp (Conditional Edge).
- *Dòng:* 26

### ⚡ `route_start(state)`
- *Dòng:* 19

### ⚡ `async router_node(state)`
- *Mô tả:* Node định tuyến ban đầu dựa trên chế độ (mode).
- *Dòng:* 15

## 📁 `universal_game_vault\src\processors\batch_importer.py`
### ⚡ `**BatchImporter**.__init__(self, game_name)`
- *Dòng:* 26

### ⚡ `**BatchImporter**._ai_handler(self, state)`
- *Mô tả:* Thuc thi logic AI bat buoc tu BaseAgent
- *Dòng:* 35

### ⚡ `**BatchImporter**._logic_handler(self, state)`
- *Mô tả:* Thuc thi logic Code bat buoc tu BaseAgent
- *Dòng:* 39

### ⚡ `**BatchImporter**.extract_text_from_docx(self, docx_path)`
- *Dòng:* 53

### ⚡ `**BatchImporter**.extract_text_from_pdf(self, pdf_path)`
- *Dòng:* 43

### ⚡ `**BatchImporter**.process_character_block(self, block)`
- *Mô tả:* Su dung LLM de sinh file Wiki Markdown chuan.
- *Dòng:* 139

### ⚡ `**BatchImporter**.run_import(self)`
- *Dòng:* 63

## 📁 `universal_game_vault\src\processors\text_parser.py`
### ⚡ `**GameAIProcessor**.__init__(self, game_name)`
- *Dòng:* 11

### ⚡ `**GameAIProcessor**.analyze_document(self, raw_content)`
- *Mô tả:* Sử dụng LLM để phân tích tài liệu và phân loại thực thể.
- *Dòng:* 17

### ⚡ `**GameAIProcessor**.update_wiki(self, structured_data)`
- *Mô tả:* Cập nhật các file Markdown trong thư mục wiki/.
- *Dòng:* 31

## 📁 `universal_game_vault\src\storage\db_manager.py`
### ⚡ `**GameDBManager**.__init__(self, game_name)`
- *Dòng:* 14

### ⚡ `**GameDBManager**.init_db(self)`
- *Mô tả:* Khoi tao cau truc bang du lieu.
- *Dòng:* 22

### ⚡ `**GameDBManager**.query_characters(self, faction, rarity)`
- *Mô tả:* Truy van nhan vat theo tieu chi.
- *Dòng:* 84

### ⚡ `**GameDBManager**.sync_from_wiki(self)`
- *Mô tả:* Doc file Markdown va dong bo vao SQLite.
- *Dòng:* 44

