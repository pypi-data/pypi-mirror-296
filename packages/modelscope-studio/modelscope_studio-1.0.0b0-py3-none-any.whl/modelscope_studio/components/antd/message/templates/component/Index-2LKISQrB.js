async function Y() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function D(e) {
  return await Y(), e().then((t) => t.default);
}
function q(e) {
  const {
    gradio: t,
    _internal: o,
    ...s
  } = e;
  return Object.keys(o).reduce((i, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const a = l[1], c = a.split("_"), _ = (...m) => {
        const b = m.map((u) => m && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
          type: u.type,
          detail: u.detail,
          timestamp: u.timeStamp,
          clientX: u.clientX,
          clientY: u.clientY,
          targetId: u.target.id,
          targetClassName: u.target.className,
          altKey: u.altKey,
          ctrlKey: u.ctrlKey,
          shiftKey: u.shiftKey,
          metaKey: u.metaKey
        } : u);
        return t.dispatch(a.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (c.length > 1) {
        let m = {
          ...s.props[c[0]] || {}
        };
        i[c[0]] = m;
        for (let u = 1; u < c.length - 1; u++) {
          const h = {
            ...s.props[c[u]] || {}
          };
          m[c[u]] = h, m = h;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = _, i;
      }
      const d = c[0];
      i[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = _;
    }
    return i;
  }, {});
}
function v() {
}
function F(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function L(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return v;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(e) {
  let t;
  return L(e, (o) => t = o)(), t;
}
const w = [];
function g(e, t = v) {
  let o;
  const s = /* @__PURE__ */ new Set();
  function i(a) {
    if (F(e, a) && (e = a, o)) {
      const c = !w.length;
      for (const _ of s)
        _[1](), w.push(_, e);
      if (c) {
        for (let _ = 0; _ < w.length; _ += 2)
          w[_][0](w[_ + 1]);
        w.length = 0;
      }
    }
  }
  function n(a) {
    i(a(e));
  }
  function l(a, c = v) {
    const _ = [a, c];
    return s.add(_), s.size === 1 && (o = t(i, n) || v), a(e), () => {
      s.delete(_), s.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: n,
    subscribe: l
  };
}
const {
  getContext: j,
  setContext: z
} = window.__gradio__svelte__internal, Z = "$$ms-gr-antd-slots-key";
function B() {
  const e = g({});
  return z(Z, e);
}
const G = "$$ms-gr-antd-context-key";
function H(e) {
  var a;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = Q(), o = T({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    o.slotKey.set(c);
  }), J();
  const s = j(G), i = ((a = y(s)) == null ? void 0 : a.as_item) || e.as_item, n = s ? i ? y(s)[i] : y(s) : {}, l = g({
    ...e,
    ...n
  });
  return s ? (s.subscribe((c) => {
    const {
      as_item: _
    } = y(l);
    _ && (c = c[_]), l.update((d) => ({
      ...d,
      ...c
    }));
  }), [l, (c) => {
    const _ = c.as_item ? y(s)[c.as_item] : y(s);
    return l.set({
      ...c,
      ..._
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const V = "$$ms-gr-antd-slot-key";
function J() {
  z(V, g(void 0));
}
function Q() {
  return j(V);
}
const M = "$$ms-gr-antd-component-slot-context-key";
function T({
  slot: e,
  index: t,
  subIndex: o
}) {
  return z(M, {
    slotKey: g(e),
    slotIndex: g(t),
    subSlotIndex: g(o)
  });
}
function Ke() {
  return j(M);
}
function W(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var R = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function o() {
      for (var n = "", l = 0; l < arguments.length; l++) {
        var a = arguments[l];
        a && (n = i(n, s(a)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return o.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var l = "";
      for (var a in n)
        t.call(n, a) && n[a] && (l = i(l, a));
      return l;
    }
    function i(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(R);
var $ = R.exports;
const x = /* @__PURE__ */ W($), {
  SvelteComponent: ee,
  assign: te,
  component_subscribe: P,
  create_component: ne,
  create_slot: se,
  destroy_component: oe,
  detach: ie,
  empty: le,
  flush: p,
  get_all_dirty_from_scope: re,
  get_slot_changes: ce,
  get_spread_object: A,
  get_spread_update: ue,
  handle_promise: ae,
  init: _e,
  insert: fe,
  mount_component: me,
  noop: f,
  safe_not_equal: de,
  transition_in: I,
  transition_out: N,
  update_await_block_branch: be,
  update_slot_base: pe
} = window.__gradio__svelte__internal;
function he(e) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function ge(e) {
  let t, o;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[1].elem_style
      )
    },
    {
      className: x(
        /*$mergedProps*/
        e[1].elem_classes,
        "ms-gr-antd-message"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[1].elem_id
      )
    },
    /*$mergedProps*/
    e[1].props,
    q(
      /*$mergedProps*/
      e[1]
    ),
    {
      content: (
        /*$mergedProps*/
        e[1].props.content || /*$mergedProps*/
        e[1].content
      )
    },
    {
      slots: (
        /*$slots*/
        e[2]
      )
    },
    {
      visible: (
        /*$mergedProps*/
        e[1].visible
      )
    },
    {
      onVisible: (
        /*func*/
        e[17]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [ye]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    i = te(i, s[n]);
  return t = new /*Message*/
  e[20]({
    props: i
  }), {
    c() {
      ne(t.$$.fragment);
    },
    m(n, l) {
      me(t, n, l), o = !0;
    },
    p(n, l) {
      const a = l & /*$mergedProps, $slots, visible*/
      7 ? ue(s, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          n[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: x(
          /*$mergedProps*/
          n[1].elem_classes,
          "ms-gr-antd-message"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          n[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && A(
        /*$mergedProps*/
        n[1].props
      ), l & /*$mergedProps*/
      2 && A(q(
        /*$mergedProps*/
        n[1]
      )), l & /*$mergedProps*/
      2 && {
        content: (
          /*$mergedProps*/
          n[1].props.content || /*$mergedProps*/
          n[1].content
        )
      }, l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          n[2]
        )
      }, l & /*$mergedProps*/
      2 && {
        visible: (
          /*$mergedProps*/
          n[1].visible
        )
      }, l & /*visible*/
      1 && {
        onVisible: (
          /*func*/
          n[17]
        )
      }]) : {};
      l & /*$$scope*/
      262144 && (a.$$scope = {
        dirty: l,
        ctx: n
      }), t.$set(a);
    },
    i(n) {
      o || (I(t.$$.fragment, n), o = !0);
    },
    o(n) {
      N(t.$$.fragment, n), o = !1;
    },
    d(n) {
      oe(t, n);
    }
  };
}
function ye(e) {
  let t;
  const o = (
    /*#slots*/
    e[16].default
  ), s = se(
    o,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(i, n) {
      s && s.m(i, n), t = !0;
    },
    p(i, n) {
      s && s.p && (!t || n & /*$$scope*/
      262144) && pe(
        s,
        o,
        i,
        /*$$scope*/
        i[18],
        t ? ce(
          o,
          /*$$scope*/
          i[18],
          n,
          null
        ) : re(
          /*$$scope*/
          i[18]
        ),
        null
      );
    },
    i(i) {
      t || (I(s, i), t = !0);
    },
    o(i) {
      N(s, i), t = !1;
    },
    d(i) {
      s && s.d(i);
    }
  };
}
function we(e) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function Ce(e) {
  let t, o, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: we,
    then: ge,
    catch: he,
    value: 20,
    blocks: [, , ,]
  };
  return ae(
    /*AwaitedMessage*/
    e[3],
    s
  ), {
    c() {
      t = le(), s.block.c();
    },
    m(i, n) {
      fe(i, t, n), s.block.m(i, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, o = !0;
    },
    p(i, [n]) {
      e = i, be(s, e, n);
    },
    i(i) {
      o || (I(s.block), o = !0);
    },
    o(i) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        N(l);
      }
      o = !1;
    },
    d(i) {
      i && ie(t), s.block.d(i), s.token = null, s = null;
    }
  };
}
function ke(e, t, o) {
  let s, i, n, {
    $$slots: l = {},
    $$scope: a
  } = t;
  const c = D(() => import("./message-CdqeaDPT.js"));
  let {
    gradio: _
  } = t, {
    props: d = {}
  } = t;
  const m = g(d);
  P(e, m, (r) => o(15, s = r));
  let {
    _internal: b = {}
  } = t, {
    content: u = ""
  } = t, {
    as_item: h
  } = t, {
    visible: C = !1
  } = t, {
    elem_id: k = ""
  } = t, {
    elem_classes: K = []
  } = t, {
    elem_style: S = {}
  } = t;
  const [E, U] = H({
    gradio: _,
    props: s,
    _internal: b,
    content: u,
    visible: C,
    elem_id: k,
    elem_classes: K,
    elem_style: S,
    as_item: h
  });
  P(e, E, (r) => o(1, i = r));
  const O = B();
  P(e, O, (r) => o(2, n = r));
  const X = (r) => {
    o(0, C = r);
  };
  return e.$$set = (r) => {
    "gradio" in r && o(7, _ = r.gradio), "props" in r && o(8, d = r.props), "_internal" in r && o(9, b = r._internal), "content" in r && o(10, u = r.content), "as_item" in r && o(11, h = r.as_item), "visible" in r && o(0, C = r.visible), "elem_id" in r && o(12, k = r.elem_id), "elem_classes" in r && o(13, K = r.elem_classes), "elem_style" in r && o(14, S = r.elem_style), "$$scope" in r && o(18, a = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && m.update((r) => ({
      ...r,
      ...d
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, content, visible, elem_id, elem_classes, elem_style, as_item*/
    65153 && U({
      gradio: _,
      props: s,
      _internal: b,
      content: u,
      visible: C,
      elem_id: k,
      elem_classes: K,
      elem_style: S,
      as_item: h
    });
  }, [C, i, n, c, m, E, O, _, d, b, u, h, k, K, S, s, l, X, a];
}
class Se extends ee {
  constructor(t) {
    super(), _e(this, t, ke, Ce, de, {
      gradio: 7,
      props: 8,
      _internal: 9,
      content: 10,
      as_item: 11,
      visible: 0,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), p();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), p();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), p();
  }
  get content() {
    return this.$$.ctx[10];
  }
  set content(t) {
    this.$$set({
      content: t
    }), p();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), p();
  }
  get visible() {
    return this.$$.ctx[0];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), p();
  }
}
export {
  Se as I,
  Ke as g,
  g as w
};
